from langgraph.graph import StateGraph, END, START
from agents.land_use_permits_agent import generate_land_use_permits
from agents.commercial_standards_agent import generate_commercial_standards
from agents.general_standards_agent import generate_general_standards
from agents.zoning_agent import generate_zoning
from agents.postprocess_agent import postprocess_document
import json 
import os


from core.template_loader import load_template, fill_template
from core.state import DocState


async def land_use_permits_node(state: DocState) -> dict:
    permits = await generate_land_use_permits(state)
    return {"land_use_permits_content": permits}

async def commercial_standards_node(state: DocState) -> dict:
    commercial = await generate_commercial_standards(state)
    return {"commercial_standards_content": commercial}

async def general_standards_node(state: DocState) -> dict:
    general = await generate_general_standards(state)
    return {"general_standards_content": general}

async def zoning_node(state: DocState) -> dict:
    zoning = await generate_zoning(state)
    return {"zoning_content": zoning}

async def postprocess_node(state: DocState) -> dict:
    template = load_template()
    filled_html = fill_template(template, {
        "org_logo_url": state.org_logo_url,
        "meeting_date": state.meeting_date,
        "staff_member_name": state.staff_member_name,
        "staff_member_designation": state.staff_member_designation,
        "staff_member_email": state.staff_member_email,
        "staff_member_phone": state.staff_member_phone,
        "staff_member_extension": state.staff_member_extension,
        "application_number": state.application_number,
        "location": state.location,
        "application_name": state.application_name,
        "zoning_district": state.zoning_district,
        "use_classification": state.use_classification,
        "project_description": state.project_description,
        "land_use_permits_content": state.land_use_permits_content,
        "commercial_standards_content": state.commercial_standards_content,
        "general_standards_content": state.general_standards_content,
        "zoning_content": state.zoning_content,
    })
    final_html = postprocess_document(filled_html)
    return {"final_document": final_html}

def load_dummy_data() -> dict:
    """Load dummy data from a JSON file."""
    dummy_path = os.path.join(os.path.dirname(__file__), "..", "static", "dummy_data.json")
    with open(dummy_path, "r", encoding="utf-8") as f:
        return json.load(f)
    

async def generate_document(doc_id: str, data: dict, store: dict) -> None:
    """Generate a document using the state graph and save it to the store."""
    dummy_data = load_dummy_data()
    combined_data = {**dummy_data, **data}
    state = DocState(**combined_data)

    graph = StateGraph(DocState)
    
    graph.add_node("generate_zoning", zoning_node)
    graph.add_node("generate_land_use_permits", land_use_permits_node)
    graph.add_node("generate_commercial_standards", commercial_standards_node)
    graph.add_node("generate_general_standards", general_standards_node)
    graph.add_node("postprocess", postprocess_node)

    # From START -> launch all content generators in parallel
    graph.add_edge(START, "generate_zoning")
    graph.add_edge(START, "generate_land_use_permits")
    graph.add_edge(START, "generate_commercial_standards")
    graph.add_edge(START, "generate_general_standards")

    # All agents → merge to Postprocess
    graph.add_edge("generate_zoning", "postprocess")
    graph.add_edge("generate_land_use_permits", "postprocess")
    graph.add_edge("generate_commercial_standards", "postprocess")
    graph.add_edge("generate_general_standards", "postprocess")

    # Postprocess → END
    graph.add_edge("postprocess", END)
    app = graph.compile()

    # Run the state graph
    result = await app.ainvoke(state)
    store[doc_id] = result["final_document"]


def get_document_by_id(doc_id: str, store: dict):
    return store.get(doc_id)
