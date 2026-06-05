from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

from scripts.character_designer import CharacterDesigner
from scripts.generate_pages import PageGenerator
from scripts.bubble_detector import BubbleDetector
from scripts.pdf_compiler import PDFCompiler
from scripts.utils import logger

app = FastAPI(title="Manga Automation Studio", description="Professional Manga Creation UI")

# Ensure output directories exist so static files can be served
os.makedirs("output/characters", exist_ok=True)
os.makedirs("output/pages/processed", exist_ok=True)

# Mount static directories

app.mount("/output", StaticFiles(directory="output"), name="output")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main dashboard."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/character/design")
def api_design_character(name: str = Form(...), description: str = Form(...)):
    """API endpoint to design a character."""
    designer = CharacterDesigner()
    file_path = designer.generate_character(name, description)
    if file_path:
        return {"status": "success", "message": f"Character {name} designed.", "image_url": f"/{file_path}"}
    return {"status": "error", "message": "Failed to generate character."}

@app.post("/api/pages/generate")
def api_generate_pages(story: str = Form(...), num_pages: int = Form(...)):
    """API endpoint to generate pages."""
    generator = PageGenerator()
    file_paths = generator.generate(story, num_pages)
    if file_paths:
        urls = [f"/{path}" for path in file_paths]
        return {"status": "success", "message": f"Generated {len(file_paths)} pages.", "image_urls": urls}
    return {"status": "error", "message": "Failed to generate pages."}

def background_process_pipeline():
    """Run bubble detection and PDF compilation."""
    logger.info("Starting background processing pipeline...")
    detector = BubbleDetector()
    detector.process_directory()

    compiler = PDFCompiler()
    compiler.compile()
    logger.info("Background processing pipeline finished.")

@app.post("/api/pipeline/process")
async def api_process_pipeline(background_tasks: BackgroundTasks):
    """API endpoint to trigger bubble detection and PDF compilation in the background."""
    background_tasks.add_task(background_process_pipeline)
    return {"status": "success", "message": "Pipeline processing started in the background."}

if __name__ == "__main__":
    logger.info("Starting Web UI Server...")
    uvicorn.run("scripts.web_ui:app", host="0.0.0.0", port=8000, reload=True)
