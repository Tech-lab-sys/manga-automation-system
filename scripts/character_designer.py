import os
import requests
import urllib.parse
from typing import Optional
from scripts.utils import logger, config

class CharacterDesigner:
    """Class responsible for designing and generating manga characters."""

    def __init__(self, output_dir: str = "output/characters"):
        self.output_dir = output_dir
        self.session = requests.Session()
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized CharacterDesigner with output directory: {self.output_dir}")

    def generate_character(self, name: str, description: str) -> Optional[str]:
        """
        Generates a character design image using Pollinations AI.

        Args:
            name (str): The name of the character.
            description (str): A detailed physical description.

        Returns:
            Optional[str]: The file path to the generated image, or None if failed.
        """
        logger.info(f"Starting design generation for character: '{name}'")
        logger.debug(f"Description provided: {description}")

        prompt = f"manga character design, {description}, anime style, high quality, concept art, full body"
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

        try:
            logger.info("Calling Pollinations.ai API...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            safe_name = name.lower().replace(' ', '_')
            file_path = os.path.join(self.output_dir, f"{safe_name}.png")

            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Character '{name}' generated successfully and saved to {file_path}")
            return file_path

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to generate character '{name}': API Request error: {e}")
        except IOError as e:
            logger.error(f"Failed to save character image to disk: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        return None

if __name__ == "__main__":
    designer = CharacterDesigner()
    designer.generate_character("Hero", "Brave young male protagonist with spiky black hair, wearing fantasy armor")
