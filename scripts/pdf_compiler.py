import os
import glob
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from scripts.utils import setup_logging, ConfigManager

logger = setup_logging("pdf_compiler")
config = ConfigManager()

class PDFCompiler:
    def __init__(self):
        self.output_dir = config.get('paths.output', './output')

    def compile(self, output_filename: str = "manga.pdf"):
        output_path = os.path.join(self.output_dir, output_filename)
        logger.info(f"Compiling PDF to {output_path}")

        try:
            image_paths = sorted(glob.glob(os.path.join(self.output_dir, "page_*.jpg")))
            if not image_paths:
                logger.warning("No pages found to compile.")
                return None

            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4

            for img_path in image_paths:
                logger.info(f"Adding {img_path} to PDF")
                c.drawImage(img_path, 0, 0, width=width, height=height, preserveAspectRatio=True)
                c.showPage()

            c.save()
            logger.info("PDF compilation successful.")
            return output_path
        except Exception as e:
            logger.error(f"Failed to compile PDF: {e}")
            return None

if __name__ == "__main__":
    compiler = PDFCompiler()
    compiler.compile()
