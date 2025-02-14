def extract_themes(text, theme_keywords):
    """Extract themes from text based on keywords"""
    detected_themes = {}
    text_lower = text.lower()
    
    for theme, keywords in theme_keywords.items():
        detected_themes[theme] = any(keyword in text_lower for keyword in keywords)
    
    return detected_themes