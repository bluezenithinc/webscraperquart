def camel_to_snake(name: str) -> str:
    """
    Converts a `camelCase` string to `snake_case`.

    Usage:
    >>> camel_to_snake("qualityRefinedTables")
    'quality_refined_tables'
    """
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def snake_to_camel(name: str) -> str:
    """
    Converts a `snake_case` string to `camelCase`.

    Usage:
    >>> snake_to_camel("quality_refined_tables")
    'qualityRefinedTables'
    """
    return name.split("_")[0] + "".join(
        [word.capitalize() for word in name.split("_")[1:]]
    )
