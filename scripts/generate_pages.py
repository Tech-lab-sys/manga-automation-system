import os
import requests
import urllib.parse
import time
from typing import List
import concurrent.futures
from scripts.utils import logger, config

class PageGenerator:
    """Class responsible for generating manga pages from a story."""

    def __init__(self, output_dir: str = "output/pages", delay: float = 1.0):
        self.output_dir = output_dir
        self.delay = delay
        self.session = requests.Session()
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized PageGenerator. Output directory: {self.output_dir}, API Delay: {self.delay}s")

    def _generate_single_page(self, i: int, story: str, num_pages: int) -> str:
        """Helper to generate a single page."""
        logger.info(f"Generating page {i}/{num_pages}...")

        prompt = f"masterpiece, best quality, monochrome, greyscale, screentone, manga page layout, multiple panels, black and white comic, {story}, scene {i}, intricate details, highly detailed lineart"
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&nologo=true"

        try:
            response = self.session.get(url, timeout=45)
            response.raise_for_status()

            file_path = os.path.join(self.output_dir, f"page_{i:03d}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Page {i} successfully generated and saved to {file_path}")

            # Simple backoff/delay (though concurrent, we still add a small sleep to avoid completely slamming the API)
            time.sleep(self.delay)
            return file_path

        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed while generating page {i}: {e}")
        except IOError as e:
            logger.error(f"Failed to save page {i} to disk: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on page {i}: {e}")
        return None

    def generate(self, story: str, num_pages: int) -> List[str]:
        """
        Generates a sequence of manga pages concurrently.

        Args:
            story (str): The overall story or context for the pages.
            num_pages (int): The number of pages to generate.

        Returns:
            List[str]: A list of file paths to the generated pages.
        """
        logger.info(f"Starting concurrent generation of {num_pages} pages for story snippet: '{story[:50]}...'")
        generated_files = []

        # Use ThreadPoolExecutor to generate pages concurrently.
        # Max workers set to 5 to avoid overwhelming the API.
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Map the helper function to all page numbers
            futures = {
                executor.submit(self._generate_single_page, i, story, num_pages): i
                for i in range(1, num_pages + 1)
            }

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    generated_files.append(result)

        # Ensure files are returned in sequential order despite concurrent execution
        generated_files.sort()
        logger.info(f"Generation complete. Successfully generated {len(generated_files)}/{num_pages} pages.")
        return generated_files

if __name__ == "__main__":
    generator = PageGenerator()
    generator.generate("epic fantasy battle scene in a ruined ancient city, swords clashing, dramatic lighting", 3)
