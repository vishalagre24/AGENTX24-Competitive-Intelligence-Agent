import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


def search_news(company):
    """
    External Tool #1
    Searches recent competitor/industry news.
    """

    query = quote(company)

    url = (
        "https://news.google.com/rss/search"
        f"?q={query}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "AGENTX24-Competitive-Intelligence-Agent/1.0"
            }
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)

        articles = []

        for item in root.findall(".//item")[:5]:

            articles.append({
                "title": item.findtext("title", ""),
                "link": item.findtext("link", ""),
                "published": item.findtext("pubDate", ""),
                "source": item.findtext("source", "")
            })

        return {
            "tool": "NEWS_SEARCH",
            "company": company,
            "results_found": len(articles),
            "results": articles
        }

    except Exception as e:

        return {
            "tool": "NEWS_SEARCH",
            "company": company,
            "results_found": 0,
            "results": [],
            "error": str(e)
        }