import os
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from scripts.utils import setup_logging
from scripts.character_designer import CharacterDesigner
from scripts.generate_pages import PageGenerator
from scripts.bubble_detector import BubbleDetector
from scripts.pdf_compiler import PDFCompiler

logger = setup_logging("web_ui")
app = FastAPI(title="Manga Automation System")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Make output accessible
os.makedirs("output", exist_ok=True)
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/generate")
def generate_manga(request: Request, story: str = Form(...), pages: int = Form(...)):
    logger.info(f"Received request to generate {pages} pages for story: {story}")

    designer = CharacterDesigner()
    generator = PageGenerator()
    detector = BubbleDetector()
    compiler = PDFCompiler()

    # 1. Consistent Character (mock step)
    char_prompt = "hero with dark hair"
    designer.design(char_prompt, "main_character")

    # 1.5 Clear previous output to prevent mixing pages
    generator.clear_output()

    # 2. Generate pages
    for i in range(1, pages + 1):
        segment = f"Part {i} of story: {story}"
        page_path = generator.generate_page(segment, i, characters=char_prompt)

        # 3. Add Speech Bubble
        if page_path:
            detector.detect_and_draw(page_path, f"Speech for {segment}")

    # 4. Compile PDF
    pdf_path = compiler.compile("manga.pdf")

    if pdf_path:
        pdf_url = "/output/manga.pdf"
        return templates.TemplateResponse(request=request, name="index.html", context={"message": "Success!", "pdf_url": pdf_url})
    else:
        return templates.TemplateResponse(request=request, name="index.html", context={"message": "Failed to generate PDF.", "error": True})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
