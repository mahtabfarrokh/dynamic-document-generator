import re



def postprocess_document(html: str) -> str:
    """Postprocess the generated HTML document."""
    print("Postprocessing document...")
    
    # Remove extra whitespace
    clean_html = re.sub(r'\s+', ' ', html).strip()
    
    return clean_html


