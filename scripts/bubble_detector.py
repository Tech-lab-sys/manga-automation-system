import os
import cv2
import textwrap
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from scripts.utils import logger, config

class BubbleDetector:
    """Class to detect and process speech bubbles in manga pages."""

    def __init__(self, input_dir: str = "output/pages", output_dir: str = "output/pages/processed"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        # Configuration for bubble detection
        self.min_area = config.get('bubble_min_area', 1000)
        self.max_area = config.get('bubble_max_area', 50000)
        self.threshold_val = config.get('bubble_threshold', 240)

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized BubbleDetector. Input: {self.input_dir}, Output: {self.output_dir}")

    def _detect_bubbles_in_image(self, img) -> List[Tuple[int, int, int, int]]:
        """Core logic to find white regions resembling speech bubbles."""
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, self.threshold_val, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            bubbles = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if self.min_area < area < self.max_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    bubbles.append((x, y, w, h))
            return bubbles
        except Exception as e:
            logger.error(f"Failed to process image array during detection: {e}")
            return []

    def _draw_bubble_with_text(self, img_pil: Image.Image, box: Tuple[int, int, int, int], text: str = "Lorem ipsum..."):
        """Draws a nice comic-style bubble and wraps text inside it using PIL."""
        draw = ImageDraw.Draw(img_pil)
        x, y, w, h = box

        # Draw white bubble with black border
        padding = 10
        bubble_box = [x - padding, y - padding, x + w + padding, y + h + padding]
        draw.ellipse(bubble_box, fill="white", outline="black", width=3)

        # Load a default font (fallback to standard if TTF not available)
        try:
            # Try to load a nice font, fallback to default
            font = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font = ImageFont.load_default()

        # Wrap text
        char_width = 8 # rough estimate
        max_chars_per_line = max(10, w // char_width)
        wrapped_lines = textwrap.wrap(text, width=max_chars_per_line)

        # Calculate vertical start to center text
        total_text_height = len(wrapped_lines) * 20 # 20px per line approx
        text_y = y + (h - total_text_height) // 2

        # Draw each line
        for line in wrapped_lines:
            # Calculate horizontal start to center text
            # Depending on Pillow version, textlength or textsize is used. Using basic approach.
            draw.text((x, text_y), line, fill="black", font=font)
            text_y += 20

        return img_pil

    def process_directory(self) -> None:
        """Scans the input directory and processes all images found."""
        logger.info(f"Scanning pages in {self.input_dir}...")

        if not os.path.exists(self.input_dir):
            logger.warning(f"Input directory {self.input_dir} does not exist.")
            return

        pages = [f for f in os.listdir(self.input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not pages:
            logger.warning("No images found to process.")
            return

        for page in sorted(pages):
            logger.info(f"Processing page: {page}")
            img_path = os.path.join(self.input_dir, page)

            try:
                img = cv2.imread(img_path)
                if img is None:
                    logger.error(f"Failed to read image {page}. Skipping.")
                    continue

                bubbles = self._detect_bubbles_in_image(img)
                logger.debug(f"Found {len(bubbles)} potential bubbles in {page}.")

                # Convert to PIL for drawing nice UI
                img_pil = Image.open(img_path).convert("RGB")

                # Fallback: if no bubbles detected, artificially place one
                if not bubbles:
                    logger.info("No bubbles detected. Adding a fallback bubble.")
                    img_w, img_h = img_pil.size
                    bubbles = [(img_w // 2 - 50, 50, 100, 50)]

                for (x, y, w, h) in bubbles:
                    self._draw_bubble_with_text(img_pil, (x, y, w, h), "Ah! What is this incredible power?!")

                out_path = os.path.join(self.output_dir, page)
                img_pil.save(out_path)
                logger.info(f"Processed {page} saved to {out_path} with {len(bubbles)} rendered bubbles.")

            except Exception as e:
                logger.error(f"Error processing {page}: {e}")

if __name__ == "__main__":
    detector = BubbleDetector()
    detector.process_directory()
