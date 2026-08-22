import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote


def search_patents(company):
    """
    Search recent patent-related information.
    """

    query = quote(company)

    url = (
        "https://patents.google.com/xhr/query"
        f"?url=q%3D{query}"
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

        data = response.json()

        results = []

        # Keep the tool defensive because patent response structures can change.
        for item in data.get("results", {}).get("cluster", [])[:5]:
            results.append(item)

        return {
            "company": company,
            "source": "Google Patents",
            "results_found": len(results),
            "findings": results
        }

    except Exception as e:
        return {
            "company": company,
            "source": "Google Patents",
            "results_found": 0,
            "findings": [],
            "error": str(e)
        }