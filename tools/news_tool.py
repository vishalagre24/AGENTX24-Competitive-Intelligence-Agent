
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


def get_competitor_news(company="OpenAI"):

    url = (
        "https://news.google.com/rss/search?"
        "q=" + quote(company + " AI competitors") +
        "&hl=en-US&gl=US&ceid=US:en"
    )

    try:

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        root = ET.fromstring(response.content)

        findings = []

        for item in root.findall(".//item")[:10]:

            title = item.findtext("title", "")
            link = item.findtext("link", "")
            published = item.findtext("pubDate", "")

            source_node = item.find("source")

            source = (
                source_node.text
                if source_node is not None
                else "Google News"
            )

            findings.append({
                "title": title,
                "source": source,
                "published": published,
                "link": link
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


search_news = get_competitor_news
