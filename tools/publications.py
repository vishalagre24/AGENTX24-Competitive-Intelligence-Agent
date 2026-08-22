import requests


def search_publications(topic):
    """
    Search recent research publications using Crossref.
    """

    url = "https://api.crossref.org/works"

    params = {
        "query": topic,
        "rows": 5,
        "sort": "published",
        "order": "desc"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
            headers={
                "User-Agent": "AGENTX24-Competitive-Intelligence-Agent/1.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        findings = []

        for item in data.get("message", {}).get("items", []):

            findings.append({
                "title": item.get("title", ["Unknown"])[0],
                "published": item.get("published-print")
                or item.get("published-online")
                or {},
                "doi": item.get("DOI", ""),
                "publisher": item.get("publisher", "")
            })

        return {
            "topic": topic,
            "source": "Crossref",
            "results_found": len(findings),
            "findings": findings
        }

    except Exception as e:

        return {
            "topic": topic,
            "source": "Crossref",
            "results_found": 0,
            "findings": [],
            "error": str(e)
        }