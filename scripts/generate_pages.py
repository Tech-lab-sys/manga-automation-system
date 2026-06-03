import os
import requests
import urllib.parse
import time

def generate_pages(story, num_pages):
    print(f"Generating {num_pages} pages for story: {story}")

    output_dir = "output/pages"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, num_pages + 1):
        print(f"Generating page {i}/{num_pages}...")

        prompt = f"manga page, {story}, scene {i}, black and white, lineart, comic book style"
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&nologo=true"

        try:
            response = requests.get(url)
            response.raise_for_status()

            file_path = os.path.join(output_dir, f"page_{i:03d}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Page {i} generated and saved to {file_path}")
            time.sleep(1)  # Be polite to the API
        except Exception as e:
            print(f"Failed to generate page {i}: {e}")

    print("Page generation complete.")

if __name__ == "__main__":
    generate_pages("epic fantasy battle scene in a ruined city", 3)
