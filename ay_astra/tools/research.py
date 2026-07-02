"""Source-backed research tool for AyAstra.

Beginner explanation:
This tool searches Semantic Scholar for academic paper metadata.
Metadata means information about a paper: title, authors, year, abstract,
venue, citation count, DOI/link, and open-access PDF link when available.

No-hallucination rule:
AyAstra must not pretend to have read a full paper if we only fetched metadata
and an abstract. So this tool clearly says what came from the source.
"""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = ",".join(
    [
        "title",
        "authors",
        "year",
        "abstract",
        "url",
        "venue",
        "publicationDate",
        "externalIds",
        "citationCount",
        "isOpenAccess",
        "openAccessPdf",
    ]
)


def get_research_brief(topic: str, limit: int = 5) -> str:
    """Return a source-backed research brief for a topic."""

    topic = topic.strip()

    if not topic:
        return _usage_message()

    if topic.lower() in {"sources", "source", "help"}:
        return _sources_message()

    source_searched = "Semantic Scholar Graph API"
    warning = ""

    try:
        papers = _search_semantic_scholar(topic, limit=limit)
    except Exception as semantic_error:
        # Semantic Scholar is excellent, but the public API can rate-limit.
        # Crossref gives us a useful fallback instead of pretending.
        try:
            papers = _search_crossref(topic, limit=limit)
            source_searched = "Crossref API fallback"
            warning = f"Semantic Scholar was unavailable: {semantic_error}"
        except Exception as crossref_error:
            return (
                f"Research Mode — {topic}\n\n"
                "I could not fetch research results right now.\n"
                f"Semantic Scholar reason: {semantic_error}\n"
                f"Crossref fallback reason: {crossref_error}\n\n"
                "Truth protocol: I will not invent papers or citations. Try again later, "
                "or use `/research sources` to see what sources this tool uses."
            )

    if not papers:
        try:
            papers = _search_crossref(topic, limit=limit)
            source_searched = "Crossref API fallback"
            warning = "Semantic Scholar returned no results, so I tried Crossref."
        except Exception as crossref_error:
            return (
                f"Research Mode — {topic}\n\n"
                "I searched Semantic Scholar but did not find results for that query, "
                "and Crossref fallback also failed.\n"
                f"Crossref reason: {crossref_error}\n\n"
                "Try a broader phrase, for example:\n"
                "- /research AI agents in education\n"
                "- /research machine learning cybersecurity\n"
                "- /research CRISPR gene editing\n\n"
                "No fake papers will be generated. The lab has standards."
            )

    if not papers:
        return (
            f"Research Mode — {topic}\n\n"
            "I searched the configured research sources but did not find results for that query.\n"
            "Try a broader phrase, for example:\n"
            "- /research AI agents in education\n"
            "- /research machine learning cybersecurity\n"
            "- /research CRISPR gene editing\n\n"
            "No fake papers will be generated. The lab has standards."
        )

    lines = [
        f"Research Mode — {topic}",
        "",
        f"Source searched: {source_searched}",
        "Truth protocol: titles, authors, years, abstracts, links, and citation counts below come from the source metadata.",
        "Important: this is not a full literature review yet. It is a starting map.",
        "",
    ]

    if warning:
        lines.extend([f"Source warning: {warning}", ""])

    for index, paper in enumerate(papers, start=1):
        metadata_source = _clean_text(paper.get("metadataSource") or source_searched)
        title = _clean_text(paper.get("title") or "Untitled")
        authors = _format_authors(paper.get("authors") or [])
        year = paper.get("year") or "year not provided"
        publication_date = paper.get("publicationDate") or "date not provided"
        venue = _clean_text(paper.get("venue") or "venue not provided")
        citation_count = paper.get("citationCount")
        citation_text = str(citation_count) if citation_count is not None else "not provided"
        abstract = _clean_text(paper.get("abstract") or "No abstract provided by source.", max_length=650)
        url = paper.get("url") or "No Semantic Scholar URL provided"
        external_ids = _format_external_ids(paper.get("externalIds") or {})
        open_access = "yes" if paper.get("isOpenAccess") else "not marked open access"
        pdf_url = _get_open_access_pdf_url(paper)

        lines.extend(
            [
                f"{index}. {title}",
                f"   Metadata source: {metadata_source}",
                f"   Authors: {authors}",
                f"   Year: {year}",
                f"   Publication date: {publication_date}",
                f"   Venue: {venue}",
                f"   Citations: {citation_text}",
                f"   Open access: {open_access}",
                f"   IDs: {external_ids}",
                f"   Abstract/summary from source: {abstract}",
                f"   Link: {url}",
            ]
        )

        if pdf_url:
            lines.append(f"   Open PDF: {pdf_url}")

        lines.append("")

    lines.extend(
        [
            "How to study these results:",
            "1. Pick the 2 most relevant titles.",
            "2. Read the abstract first, not the whole paper immediately. We are strategic, not chaotic.",
            "3. Write down 5 unfamiliar terms.",
            "4. Ask AyAstra `/tutor TERM` for each term.",
            "5. If you download a PDF later, we can build PDF summarisation as a future upgrade.",
            "",
            "AyAstra note: I used source metadata. I did not invent papers, authors, or citations.",
        ]
    )

    return "\n".join(lines).strip()


def _search_semantic_scholar(topic: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "query": topic,
            "limit": max(1, min(limit, 10)),
            "fields": SEMANTIC_SCHOLAR_FIELDS,
        }
    )
    url = f"{SEMANTIC_SCHOLAR_SEARCH_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AyAstra-QuantaCore/0.1 (+personal student project)",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_json = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        if error.code == 429:
            raise RuntimeError("Semantic Scholar rate limit reached. Wait a bit and try again.") from error
        raise RuntimeError(f"Semantic Scholar HTTP {error.code}: {body[:250]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"network error: {error.reason}") from error

    data = json.loads(raw_json)
    papers = data.get("data", [])

    if not isinstance(papers, list):
        return []

    cleaned_papers: list[dict[str, Any]] = []
    for paper in papers:
        if isinstance(paper, dict):
            paper["metadataSource"] = "Semantic Scholar"
            cleaned_papers.append(paper)

    return cleaned_papers


def _search_crossref(topic: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "query": topic,
            "rows": max(1, min(limit, 10)),
            "select": "title,author,published-print,published-online,published,container-title,publisher,abstract,DOI,URL,is-referenced-by-count,license",
        }
    )
    url = f"https://api.crossref.org/works?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AyAstra-QuantaCore/0.1 (mailto:student@example.com)",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_json = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Crossref HTTP {error.code}: {body[:250]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"network error: {error.reason}") from error

    data = json.loads(raw_json)
    items = data.get("message", {}).get("items", [])

    if not isinstance(items, list):
        return []

    normalized: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        title = _first_list_value(item.get("title")) or "Untitled"
        doi = str(item.get("DOI") or "").strip()
        url_value = str(item.get("URL") or "").strip()
        if not url_value and doi:
            url_value = f"https://doi.org/{doi}"

        normalized.append(
            {
                "metadataSource": "Crossref",
                "title": title,
                "authors": _crossref_authors(item.get("author") or []),
                "year": _crossref_year(item),
                "abstract": item.get("abstract") or "No abstract provided by source.",
                "url": url_value or "No URL provided",
                "venue": _first_list_value(item.get("container-title")) or item.get("publisher") or "venue not provided",
                "publicationDate": _crossref_publication_date(item),
                "externalIds": {"DOI": doi} if doi else {},
                "citationCount": item.get("is-referenced-by-count"),
                "isOpenAccess": bool(item.get("license")),
                "openAccessPdf": None,
            }
        )

    return normalized


def _usage_message() -> str:
    return (
        "Research Mode needs a topic.\n\n"
        "Try:\n"
        "- /research AI agents in education\n"
        "- /research CRISPR gene editing\n"
        "- /research machine learning cybersecurity\n"
        "- /research sources"
    )


def _sources_message() -> str:
    return (
        "Research Mode sources currently configured:\n\n"
        "- Semantic Scholar Graph API\n"
        "  Website: https://www.semanticscholar.org/\n"
        "  API docs: https://api.semanticscholar.org/api-docs/\n\n"
        "- Crossref API fallback\n"
        "  Website: https://www.crossref.org/\n"
        "  API docs: https://api.crossref.org/\n\n"
        "This tool fetches paper metadata and abstracts when available.\n"
        "It does not replace reading the full paper. Tiny academic detail. Massive difference."
    )


def _first_list_value(value: Any) -> str:
    if isinstance(value, list) and value:
        return _clean_text(value[0])
    return _clean_text(value)


def _crossref_authors(authors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []

    for author in authors:
        if not isinstance(author, dict):
            continue

        literal = author.get("name")
        if literal:
            normalized.append({"name": literal})
            continue

        given = _clean_text(author.get("given") or "")
        family = _clean_text(author.get("family") or "")
        name = " ".join(part for part in [given, family] if part).strip()
        if name:
            normalized.append({"name": name})

    return normalized


def _crossref_year(item: dict[str, Any]) -> int | str:
    for key in ["published-print", "published-online", "published"]:
        date_parts = item.get(key, {}).get("date-parts") if isinstance(item.get(key), dict) else None
        if isinstance(date_parts, list) and date_parts and isinstance(date_parts[0], list) and date_parts[0]:
            return date_parts[0][0]
    return "year not provided"


def _crossref_publication_date(item: dict[str, Any]) -> str:
    for key in ["published-print", "published-online", "published"]:
        date_parts = item.get(key, {}).get("date-parts") if isinstance(item.get(key), dict) else None
        if isinstance(date_parts, list) and date_parts and isinstance(date_parts[0], list):
            parts = [str(part) for part in date_parts[0]]
            return "-".join(parts)
    return "date not provided"


def _format_authors(authors: list[dict[str, Any]]) -> str:
    names = [_clean_text(author.get("name", "")) for author in authors if isinstance(author, dict)]
    names = [name for name in names if name]

    if not names:
        return "authors not provided"

    if len(names) <= 5:
        return ", ".join(names)

    return ", ".join(names[:5]) + f", and {len(names) - 5} more"


def _format_external_ids(external_ids: dict[str, Any]) -> str:
    if not external_ids:
        return "not provided"

    preferred_keys = ["DOI", "ArXiv", "PubMed", "CorpusId"]
    parts: list[str] = []

    for key in preferred_keys:
        value = external_ids.get(key)
        if value:
            parts.append(f"{key}: {value}")

    if not parts:
        for key, value in list(external_ids.items())[:3]:
            parts.append(f"{key}: {value}")

    return "; ".join(parts) if parts else "not provided"


def _get_open_access_pdf_url(paper: dict[str, Any]) -> str:
    pdf_data = paper.get("openAccessPdf")

    if not isinstance(pdf_data, dict):
        return ""

    return str(pdf_data.get("url") or "").strip()


def _clean_text(text: Any, max_length: int | None = None) -> str:
    cleaned = html.unescape(str(text or ""))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if max_length and len(cleaned) > max_length:
        return cleaned[: max_length - 1].rstrip() + "…"

    return cleaned
