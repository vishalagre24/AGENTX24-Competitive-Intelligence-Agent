def decide_task(user_input):
    """
    Decide which research sources are required.
    """

    text = user_input.lower()

    tasks = []

    # News / competitor activity
    if any(word in text for word in [
        "news",
        "competitor",
        "competitors",
        "industry",
        "market",
        "strategy",
        "activity"
    ]):
        tasks.append("NEWS_SEARCH")

    # Patent research
    if any(word in text for word in [
        "patent",
        "patents",
        "intellectual property",
        "ip"
    ]):
        tasks.append("PATENT_SEARCH")

    # Scientific/research publications
    if any(word in text for word in [
        "research",
        "publication",
        "publications",
        "paper",
        "papers",
        "scientific",
        "technology"
    ]):
        tasks.append("RESEARCH_SEARCH")

    # If nothing specific was detected
    if not tasks:
        tasks.append("NEWS_SEARCH")

    # Multiple sources
    if len(tasks) > 1:
        return "MULTI_SOURCE_RESEARCH"

    return tasks[0]