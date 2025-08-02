def detect_category_and_tags(content):
    # Simple keyword detection for demonstration
    tags = []
    if "finance" in content.lower():
        category = "Finance"
        tags = ["money", "finance", "investment"]
    elif "technology" in content.lower():
        category = "Technology"
        tags = ["tech", "AI", "gadgets"]
    else:
        category = "General"
        tags = ["trending", "news"]
    return category, tags