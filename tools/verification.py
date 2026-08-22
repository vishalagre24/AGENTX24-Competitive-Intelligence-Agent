def verify_report(report, research_results):
    """
    Verify that the agent produced a useful report
    from available research results.
    """

    if not report or not report.strip():
        return {
            "verified": False,
            "reason": "Empty report"
        }

    if not research_results:
        return {
            "verified": False,
            "reason": "No research data available"
        }

    report_lower = report.lower()

    required_sections = [
        "key findings",
        "recommended actions"
    ]

    missing_sections = [
        section
        for section in required_sections
        if section not in report_lower
    ]

    if missing_sections:
        return {
            "verified": False,
            "reason": f"Missing sections: {missing_sections}"
        }

    return {
        "verified": True,
        "reason": "Report passed basic verification"
    }