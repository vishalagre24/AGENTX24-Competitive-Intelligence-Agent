def decide_tools(user_input):
    """
    Dynamically decide which external tools are relevant
    to the user's research goal.
    """

    text = user_input.lower()

    selected_tools = []

    # News / competitor activity
    if any(word in text for word in [
        "news",
        "latest",
        "announcement",
        "competitor",
        "activity",
        "update",
        "track"
    ]):
        selected_tools.append("NEWS_SEARCH")

    # Scientific research
    if any(word in text for word in [
        "research",
        "paper",
        "papers",
        "publication",
        "scientific",
        "study",
        "academic"
    ]):
        selected_tools.append("RESEARCH_SEARCH")

    # Default: competitor tracking uses news
    if not selected_tools:
        selected_tools.append("NEWS_SEARCH")

    return selected_tools


# Keep Task 1 compatibility
def decide_task(user_input):
    text = user_input.lower()

    if "track" in text:
        return "COMPETITOR_RESEARCH"

    return "GENERAL"