from core.state import DocState
from pydantic import BaseModel

from litellm import acompletion
from pydantic import ValidationError



class ZoningContent(BaseModel):
    html_section: str  # Full styled HTML block


async def generate_zoning(data: DocState, mock_response=None) -> str:
    print("starting zoning generation")
    response = await acompletion(
        model="gpt-4o-mini",  
        messages=[
            {
                "role": "system",
                "content": (
                    """You are a professional assistant generating parts of a pre-application review document for a city planning department.
                    You must generate valid HTML **content only**, intended to be inserted inside an existing <div class="ai-section">.
                    Do NOT create <html>, <head>, <body>, <div> or any surrounding structure.
                    Only generate realistic and professional text for the requested section, using correct and simple HTML tags like <p>, <ul>, <li>, <h3> if needed.
                    Keep it short, max 50 words.
                    Respond strictly as the provided response format a single field 'html_section'."""
                )
            },
            {
                "role": "user",
                "content": (
                    "Generate the Zoning section content."
                    "You may generate multiple nested subsections if needed."
                    "Make it realistic, clear, and professional. Keep it concise."
                )
            }
        ],
        temperature=0.2,
        response_format=ZoningContent, 
        mock_response=mock_response
    )

    json_content = response.choices[0].message.content

    try:
        validated = ZoningContent.parse_raw(json_content)
        print("finished zoning generation")
        return validated.html_section
    except ValidationError as e:
        print("Validation error:", e)
        raise ValueError("Model output could not be parsed into expected structure.")
   
