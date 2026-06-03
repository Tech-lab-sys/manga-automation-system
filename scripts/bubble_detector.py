import os
import cv2
from typing import List, Tuple
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

                # Draw bounding boxes and mock text for visualization
                for (x, y, w, h) in bubbles:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Text", (x+10, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                out_path = os.path.join(self.output_dir, page)
                cv2.imwrite(out_path, img)
                logger.info(f"Processed {page} saved to {out_path} with {len(bubbles)} detected bubbles.")

            except Exception as e:
                logger.error(f"Error processing {page}: {e}")

if __name__ == "__main__":
    detector = BubbleDetector()
    detector.process_directory()
