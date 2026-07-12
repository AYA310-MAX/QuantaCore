"""Verified news/RSS tool for AyAstra.

Beginner explanation:
This tool fetches real headlines from RSS/Atom feeds published by news sites.
RSS is like a website's official "latest updates list" in XML format.

Why this helps with no hallucinations:
AyAstra does not invent headlines. It fetches source-provided titles,
summaries, dates, and links, then shows them to Ayanda.
"""

from __future__ import annotations

import html
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable


@dataclass(frozen=True)
class NewsSource:
    name: str
    url: str
    categories: tuple[str, ...]


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    source: str
    published: str
    summary: str
    sort_date: datetime | None


NEWS_SOURCES: tuple[NewsSource, ...] = (
    NewsSource(
        name="BBC News — Technology",
        url="https://feeds.bbci.co.uk/news/technology/rss.xml",
        categories=("tech", "technology", "ai", "global"),
    ),
    NewsSource(
        name="The Verge",
        url="https://www.theverge.com/rss/index.xml",
        categories=("tech", "technology", "ai", "gadgets", "global"),
    ),
    NewsSource(
        name="Ars Technica",
        url="https://feeds.arstechnica.com/arstechnica/index",
        categories=("tech", "technology", "science", "ai", "cybersecurity", "global"),
    ),
    NewsSource(
        name="Hacker News Front Page",
        url="https://hnrss.org/frontpage",
        categories=("tech", "programming", "software", "startup", "ai"),
    ),
    NewsSource(
        name="TechCentral South Africa",
        url="https://techcentral.co.za/feed/",
        categories=("south africa", "za", "tech", "technology", "telecoms"),
    ),
)

TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "ai": (
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "chatgpt",
        "openai",
        "google deepmind",
        "model",
        "neural",
        "agent",
    ),
    "artificial intelligence": (
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "chatgpt",
        "openai",
        "model",
    ),
    "biotech": (
        "biotech",
        "biotechnology",
        "gene",
        "genetic",
        "crispr",
        "biology",
        "drug",
        "medicine",
        "vaccine",
        "clinical",
        "health",
    ),
    "software": (
        "software",
        "developer",
        "programming",
        "github",
        "python",
        "javascript",
        "java",
        "coding",
    ),
    "cybersecurity": (
        "cybersecurity",
        "security",
        "cyber",
        "hack",
        "breach",
        "ransomware",
        "malware",
        "vulnerability",
    ),
    "south africa": (
        "south africa",
        "south african",
        "za",
        "eskom",
        "telkom",
        "vodacom",
        "mtn",
        "rain",
        "takealot",
        "naspers",
        "capitec",
        "load shedding",
        "sars",
    ),
    "za": (
        "south africa",
        "south african",
        "eskom",
        "telkom",
        "vodacom",
        "mtn",
        "rain",
        "takealot",
        "naspers",
        "capitec",
    ),
}

GENERIC_TOPICS = {"", "tech", "technology", "updates", "news", "today", "global"}


def get_news_brief(topic: str = "technology", limit: int = 5) -> str:
    """Fetch and format a source-backed news brief."""

    normalized_topic = topic.strip().lower() or "technology"

    if normalized_topic in {"sources", "source", "list"}:
        return list_news_sources()

    sources = _select_sources(normalized_topic)
    all_items: list[NewsItem] = []
    errors: list[str] = []

    for source in sources:
        try:
            all_items.extend(_fetch_source_items(source))
        except Exception as error:  # Keep one broken feed from killing the whole brief.
            errors.append(f"{source.name}: {error}")

    filtered_items = _filter_items(all_items, normalized_topic)
    deduped_items = _deduplicate_items(filtered_items)
    sorted_items = sorted(
        deduped_items,
        key=lambda item: item.sort_date or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    selected_items = sorted_items[:limit]

    checked_sources = ", ".join(source.name for source in sources)

    if not selected_items:
        message = (
            f"Verified News Brief — {topic}\n\n"
            f"I checked these source feeds: {checked_sources}.\n\n"
            "I did not find matching items in the current feed results. "
            "Try `/news tech`, `/news ai`, `/news software`, `/news cybersecurity`, "
            "or `/news sources`."
        )
        if errors:
            message += "\n\nFeed warnings:\n" + "\n".join(f"- {error}" for error in errors)
        return message

    lines = [
        f"Verified News Brief — {topic}",
        "",
        f"Checked source feeds: {checked_sources}",
        "Truth protocol: headlines, dates, links, and summaries below come from the RSS/Atom feeds.",
        "",
    ]

    for index, item in enumerate(selected_items, start=1):
        published = item.published or "date not provided in feed"
        summary = item.summary or "No feed summary provided. Open the source link for the full article."

        lines.extend(
            [
                f"{index}. {item.title}",
                f"   Source: {item.source}",
                f"   Published: {published}",
                f"   Summary from feed: {summary}",
                f"   Link: {item.link}",
                "",
            ]
        )

    if errors:
        lines.append("Feed warnings:")
        lines.extend(f"- {error}" for error in errors)
        lines.append("")

    lines.append("AyAstra note: I fetched these from source feeds; I did not invent the headlines. Very important, obviously.")
    return "\n".join(lines).strip()


def list_news_sources() -> str:
    """Return the configured news sources."""

    lines = ["Configured verified news feeds:", ""]
    for source in NEWS_SOURCES:
        lines.append(f"- {source.name}")
        lines.append(f"  Categories: {', '.join(source.categories)}")
        lines.append(f"  Feed: {source.url}")
    lines.extend(
        [
            "",
            "Try:",
            "/news tech",
            "/news ai",
            "/news south africa",
            "/news software",
            "/news cybersecurity",
        ]
    )
    return "\n".join(lines)


def _select_sources(topic: str) -> tuple[NewsSource, ...]:
    # For South African context, prioritize TechCentral but still allow global tech feeds
    # when they contain matching South African keywords.
    if topic in {"south africa", "za", "south african"}:
        return NEWS_SOURCES

    matching_sources = [source for source in NEWS_SOURCES if topic in source.categories]
    if matching_sources:
        return tuple(matching_sources)

    # Unknown topic: search all feeds and filter by topic words.
    return NEWS_SOURCES


def _fetch_source_items(source: NewsSource) -> list[NewsItem]:
    request = urllib.request.Request(
        source.url,
        headers={
            "User-Agent": "AyAstra-QuantaCore/0.1 (+personal student project)",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw_xml = response.read()
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"network error: {error.reason}") from error

    root = ET.fromstring(raw_xml)

    if _local_name(root.tag) == "feed":
        return _parse_atom_feed(root, source)

    return _parse_rss_feed(root, source)


def _parse_rss_feed(root: ET.Element, source: NewsSource) -> list[NewsItem]:
    items: list[NewsItem] = []

    for item in _iter_elements_by_local_name(root, "item"):
        title = _clean_text(_find_child_text(item, "title"))
        link = _clean_text(_find_child_text(item, "link"))
        published = _clean_text(_find_child_text(item, "pubDate") or _find_child_text(item, "date"))
        summary = _clean_summary(_find_child_text(item, "description") or _find_child_text(item, "summary"))

        if title and link:
            items.append(
                NewsItem(
                    title=title,
                    link=link,
                    source=source.name,
                    published=published,
                    summary=summary,
                    sort_date=_parse_date(published),
                )
            )

    return items


def _parse_atom_feed(root: ET.Element, source: NewsSource) -> list[NewsItem]:
    items: list[NewsItem] = []

    for entry in _iter_elements_by_local_name(root, "entry"):
        title = _clean_text(_find_child_text(entry, "title"))
        link = _find_atom_link(entry)
        published = _clean_text(
            _find_child_text(entry, "published") or _find_child_text(entry, "updated")
        )
        summary = _clean_summary(
            _find_child_text(entry, "summary") or _find_child_text(entry, "content")
        )

        if title and link:
            items.append(
                NewsItem(
                    title=title,
                    link=link,
                    source=source.name,
                    published=published,
                    summary=summary,
                    sort_date=_parse_date(published),
                )
            )

    return items


def _filter_items(items: Iterable[NewsItem], topic: str) -> list[NewsItem]:
    if topic in GENERIC_TOPICS:
        return list(items)

    keywords = TOPIC_KEYWORDS.get(topic)
    if not keywords:
        keywords = tuple(word for word in re.split(r"\s+", topic) if len(word) >= 3)

    filtered: list[NewsItem] = []

    for item in items:
        searchable_text = f"{item.title} {item.summary} {item.source}".lower()

        # TechCentral is a South African tech feed, so all of it is relevant for /news south africa.
        if topic in {"south africa", "za", "south african"} and item.source == "TechCentral South Africa":
            filtered.append(item)
            continue

        if any(_keyword_in_text(keyword, searchable_text) for keyword in keywords):
            filtered.append(item)

    return filtered


def _keyword_in_text(keyword: str, text: str) -> bool:
    """Return True when a keyword appears in text without silly short-word matches.

    Example: South African mobile network `rain` should not match the word `train`.
    Tiny detail, big difference. The lab approves.
    """

    keyword = keyword.lower().strip()
    if not keyword:
        return False

    if " " in keyword or len(keyword) <= 4:
        pattern = rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])"
        return re.search(pattern, text) is not None

    return keyword in text


def _deduplicate_items(items: Iterable[NewsItem]) -> list[NewsItem]:
    seen: set[str] = set()
    deduped: list[NewsItem] = []

    for item in items:
        key = item.link or item.title.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    return deduped


def _find_child_text(element: ET.Element, child_name: str) -> str:
    for child in element:
        if _local_name(child.tag) == child_name:
            return "".join(child.itertext())
    return ""


def _find_atom_link(entry: ET.Element) -> str:
    for child in entry:
        if _local_name(child.tag) != "link":
            continue
        href = child.attrib.get("href", "").strip()
        if href:
            return href
        text = _clean_text("".join(child.itertext()))
        if text:
            return text
    return ""


def _iter_elements_by_local_name(root: ET.Element, name: str) -> Iterable[ET.Element]:
    for element in root.iter():
        if _local_name(element.tag) == name:
            yield element


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _clean_summary(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return _clean_text(text, max_length=280)


def _clean_text(text: str, max_length: int | None = None) -> str:
    cleaned = html.unescape(text or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if max_length and len(cleaned) > max_length:
        return cleaned[: max_length - 1].rstrip() + "…"

    return cleaned


def _parse_date(value: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None

    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (TypeError, ValueError):
        pass

    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None
