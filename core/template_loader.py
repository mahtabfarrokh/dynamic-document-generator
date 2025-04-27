from pathlib import Path
import re

TEMPLATE_PATH = Path(__file__).parent.parent / "static" / "template.html"

def load_template() -> str:
    """Load the static HTML template."""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def fill_template(template: str, fields: dict) -> str:
    """Safely fill placeholders in the template with given fields."""
    def replacer(match):
        key = match.group(1).strip()
        return fields.get(key, "")  # If missing, replace with empty string

    pattern = re.compile(r"\{\{(.*?)\}\}")  # Match {{ key }}
    return pattern.sub(replacer, template)

