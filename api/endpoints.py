from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from core.orchestrator import generate_document, get_document_by_id
from fastapi.responses import HTMLResponse


router = APIRouter()

# Simple in-memory store for generated docs
documents_store = {}

class DocumentRequest(BaseModel):
    request_id: str  # Unique id for the request (you can send random UUID from client)
    data: dict       # Dynamic fields that will fill the template (later can be expanded)

@router.post("/generate")
async def generate_document_endpoint(request: DocumentRequest, background_tasks: BackgroundTasks):
    # Trigger background generation
    background_tasks.add_task(generate_document, request.request_id, request.data, documents_store)
    return {"message": "Document generation started", "request_id": request.request_id}

@router.get("/get/{doc_id}")
async def get_document(doc_id: str):
    document = get_document_by_id(doc_id, documents_store)
    if document:
        return {"document_html": document}
    else:
        return {"error": "Document not found"}

@router.get("/view/{doc_id}", response_class=HTMLResponse)
async def view_document(doc_id: str):
    document = get_document_by_id(doc_id, documents_store)
    print(document)
    if document:
        return HTMLResponse(content=document, status_code=200)
    else:
        return {"error": "Document not found"}