import requests


def search_research(topic):
    """
    External Tool #2
    Searches scientific publications using Crossref.
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

        items = data.get("message", {}).get("items", [])

        results = []

        for item in items:
            titles = item.get("title", [])

            title = titles[0] if titles else "Unknown title"

            results.append({
                "title": title,
                "doi": item.get("DOI", ""),
                "publisher": item.get("publisher", ""),
                "type": item.get("type", "")
            })

        return {
            "tool": "RESEARCH_SEARCH",
            "topic": topic,
            "results_found": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "tool": "RESEARCH_SEARCH",
            "topic": topic,
            "results_found": 0,
            "results": [],
            "error": str(e)
        }