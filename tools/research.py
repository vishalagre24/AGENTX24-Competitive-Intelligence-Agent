import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


def research_competitor(company):
    """
    Real-time competitor research using Google News RSS.
    Returns recent news items for the requested company.
    """

    query = quote(f"{company} AI technology competitor")

    url = (
        "https://news.google.com/rss/search?"
        f"q={query}&hl=en-US&gl=US&ceid=US:en"
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

        findings = []

        for item in root.findall(".//item")[:8]:

            title = item.findtext("title")
            link = item.findtext("link")
            published = item.findtext("pubDate")
            source = item.findtext("source")

            if title:
                findings.append({
                    "title": title,
                    "source": source or "Unknown",
                    "published": published or "Unknown",
                    "link": link or ""
                })

        return {
            "company": company,
            "source": "Google News RSS",
            "results_found": len(findings),
            "findings": findings
        }

    except Exception as e:

        return {
            "company": company,
            "source": "Google News RSS",
            "results_found": 0,
            "findings": [],
            "error": str(e)
        }