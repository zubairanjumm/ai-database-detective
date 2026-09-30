import re


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
}


class SQLValidator:
    def validate(self, query: str) -> tuple[bool, str]:
        normalized = re.sub(r"\s+", " ", query.strip()).upper()

        if not normalized:
            return False, "Query is empty."

        if not normalized.startswith("SELECT"):
            return False, "Only SELECT queries are allowed."

        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", normalized):
                return False, f"Forbidden SQL keyword: {keyword}"

        return True, "Query is valid."