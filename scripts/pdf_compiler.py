import os
from typing import List
from PIL import Image
from scripts.utils import logger, config

# Attempt to load ReportLab for high-quality PDF generation
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not found. Will fallback to PIL for PDF compilation.")

class PDFCompiler:
    """Class responsible for compiling a series of images into a single PDF document."""

    def __init__(self, output_filename: str = "output/manga.pdf", input_dir: str = "output/pages"):
        self.output_filename = output_filename
        self.input_dir = input_dir
        self.use_reportlab = REPORTLAB_AVAILABLE

        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_filename), exist_ok=True)
        logger.info(f"Initialized PDFCompiler. Output: {self.output_filename}, Input: {self.input_dir}")

    def _get_images_to_compile(self) -> List[str]:
        """Determine which directory to read images from and return the list of image files."""
        if not os.path.exists(self.input_dir):
            logger.error(f"Input directory {self.input_dir} does not exist.")
            return []

        # Prefer processed images (with detected bubbles) if available
        processed_dir = os.path.join(self.input_dir, "processed")
        target_dir = processed_dir if os.path.exists(processed_dir) and os.listdir(processed_dir) else self.input_dir

        logger.info(f"Sourcing images from directory: {target_dir}")
        images = [f for f in os.listdir(target_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        images.sort() # Ensure chronological order

        return [os.path.join(target_dir, img) for img in images]

    def _compile_with_pil(self, image_paths: List[str]) -> bool:
        """Fallback method to compile PDF using Python Imaging Library (PIL)."""
        logger.info("Using PIL to compile PDF...")
        try:
            img_list = []
            for path in image_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img_list.append(img)

            if img_list:
                img_list[0].save(self.output_filename, save_all=True, append_images=img_list[1:])
                logger.info(f"PDF successfully compiled via PIL and saved to {self.output_filename}")
                return True
        except Exception as e:
            logger.error(f"Error saving PDF with PIL: {e}")
        return False

    def _compile_with_reportlab(self, image_paths: List[str]) -> bool:
        """Primary method to compile PDF using ReportLab with preserved aspect ratios."""
        logger.info("Using ReportLab to compile PDF...")
        try:
            c = canvas.Canvas(self.output_filename, pagesize=letter)
            page_width, page_height = letter

            for path in image_paths:
                # Open image with PIL to get original dimensions
                with Image.open(path) as img:
                    img_width, img_height = img.size

                # Calculate scaling factor to fit within page while maintaining aspect ratio
                width_ratio = page_width / img_width
                height_ratio = page_height / img_height
                scale = min(width_ratio, height_ratio)

                new_width = img_width * scale
                new_height = img_height * scale

                # Calculate centering offsets
                x_offset = (page_width - new_width) / 2
                y_offset = (page_height - new_height) / 2

                # Draw the image
                c.drawImage(path, x_offset, y_offset, width=new_width, height=new_height)
                c.showPage()

            c.save()
            logger.info(f"PDF successfully compiled via ReportLab and saved to {self.output_filename}")
            return True
        except Exception as e:
            logger.error(f"Error creating PDF with ReportLab: {e}")
            return False

    def compile(self) -> None:
        """Orchestrates the PDF compilation process."""
        image_paths = self._get_images_to_compile()

        if not image_paths:
            logger.warning(f"No valid images found to compile. Aborting PDF generation.")
            return

        logger.info(f"Found {len(image_paths)} images to compile into PDF.")

        success = False
        if self.use_reportlab:
            success = self._compile_with_reportlab(image_paths)

        # If ReportLab fails or is unavailable, fallback to PIL
        if not success:
            logger.info("Attempting compilation using PIL fallback...")
            success = self._compile_with_pil(image_paths)

        if not success:
            logger.error("All PDF compilation methods failed.")

if __name__ == "__main__":
    compiler = PDFCompiler()
    compiler.compile()
