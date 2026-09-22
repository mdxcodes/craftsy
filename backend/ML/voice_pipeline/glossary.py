"""
Craft Glossary for Voice Pipeline.

Provides craft-specific vocabulary hints for Whisper STT biasing.
"""


def build_prompt_hint(category: str, limit: int = 30, language_code: str = "en") -> str:
    """
    Build a glossary prompt hint for Whisper STT.

    Args:
        category: Craft category (e.g., "Pottery", "Textiles")
        limit: Maximum number of terms
        language_code: Language code

    Returns:
        Formatted glossary prompt string
    """
    terms = get_glossary_terms(category=category, limit=limit)
    if not terms:
        return ""
    return "Vocabulary hints: " + ", ".join(t.capitalize() for t in terms)


def get_glossary_terms(category: Optional[str] = None, limit: int = 30) -> list:
    """
    Get craft glossary terms for a category.

    Args:
        category: Optional craft category filter
        limit: Maximum number of terms

    Returns:
        List of glossary terms
    """
    glossary = {
        "pottery": [
            "terracotta", "potter's wheel", "kiln", "clay", "ceramic",
            "glaze", "earthenware", "stoneware", "porcelain", "pottery wheel",
            "slip", "bisque", "firing", "kiln-fired", "hand-thrown",
        ],
        "textiles": [
            "handloom", "weaving", "warp", "weft", "shuttle", "loom",
            "silk", "cotton", "wool", "embroidery", "block printing",
            "ikat", "bandhani", "zari", "brocade", "muslin", "chanderi",
        ],
        "jewelry": [
            "filigree", "meenakari", "kundan", "polki", "temple jewelry",
            "oxidized", "beaded", "gold-plated", "silver", "brass",
        ],
        "woodwork": [
            "carving", "wood inlay", "lacquer", "sanding", "polishing",
            "sheesham", "rosewood", "teak", "mango wood", "walnut",
        ],
        "metalwork": [
            "lost-wax casting", "dhokra", "repousse", "chasing",
            "engraving", "oxidation", "patina",
        ],
        "bamboo craft": [
            "bamboo", "cane", "wicker", "basketry", "mat weaving",
            "lamp shade", "furniture",
        ],
        "leather craft": [
            "leather", "embossing", "tooling", "stitching", "dyeing",
            "block printing", "punching",
        ],
    }

    if category and category.lower() in glossary:
        terms = glossary[category.lower()][:limit]
        return [t.capitalize() for t in terms]

    # Return all terms if no category specified
    all_terms = []
    for terms_list in glossary.values():
        all_terms.extend(terms_list)
    return [t.capitalize() for t in all_terms[:limit]]
