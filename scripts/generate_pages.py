import os
import requests
import urllib.parse
from scripts.utils import setup_logging, ConfigManager

logger = setup_logging("page_generator")
config = ConfigManager()

class PageGenerator:
    def __init__(self):
        self.output_dir = config.get('paths.output', './output')
        self.api_base = config.get('api.pollinations', 'https://image.pollinations.ai/prompt/')

    def clear_output(self):
        import glob
        logger.info("Clearing previous output pages...")
        for f in glob.glob(os.path.join(self.output_dir, "page_*.jpg")):
            try:
                os.remove(f)
            except Exception as e:
                logger.error(f"Error removing {f}: {e}")

    def generate_page(self, story_segment: str, page_num: int, characters: str = ""):
        logger.info(f"Generating page {page_num} for story: {story_segment}")
        full_prompt = f"manga page, {story_segment}, {characters}, black and white lineart, high contrast, screentones, masterpiece, highly detailed"
        encoded_prompt = urllib.parse.quote(full_prompt)
        url = f"{self.api_base}{encoded_prompt}?width=800&height=1200&nologo=true"

        try:
            # response = requests.get(url)
            # response.raise_for_status()

            # Use mock image logic
            from PIL import Image
            filepath = os.path.join(self.output_dir, f"page_{page_num:03d}.jpg")
            img = Image.new('RGB', (800, 1200), color=(200, 200, 200))
            img.save(filepath)

            logger.info(f"Mocked generated page to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to generate mock page {page_num}: {e}")
            return None

if __name__ == "__main__":
    generator = PageGenerator()
    generator.generate_page("The hero arrives at the dark castle.", 1)
