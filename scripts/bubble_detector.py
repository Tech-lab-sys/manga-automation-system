import os
from PIL import Image, ImageDraw, ImageFont
from scripts.utils import setup_logging

logger = setup_logging("bubble_detector")

class BubbleDetector:
    def __init__(self):
        pass

    def detect_and_draw(self, image_path: str, text: str):
        logger.info(f"Adding speech bubble to {image_path}")
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # Draw a mock bubble at top center
            width, height = img.size
            bubble_x1 = width * 0.1
            bubble_y1 = height * 0.05
            bubble_x2 = width * 0.9
            bubble_y2 = height * 0.2

            draw.rectangle([bubble_x1, bubble_y1, bubble_x2, bubble_y2], fill="white", outline="black", width=3)

            # Add text
            try:
                # Try to use a larger font if possible
                font = ImageFont.truetype("arial.ttf", 24)
            except IOError:
                font = ImageFont.load_default()

            # Simple text wrapping could go here, for MVP just draw it centered
            text_x = bubble_x1 + 20
            text_y = bubble_y1 + 20
            draw.text((text_x, text_y), text, fill="black", font=font)

            img.save(image_path)
            logger.info("Successfully added speech bubble")
            return image_path
        except Exception as e:
            logger.error(f"Failed to add speech bubble: {e}")
            return None

if __name__ == "__main__":
    pass # Needs an actual image to test
