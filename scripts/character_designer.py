import os
import requests
import urllib.parse

def design_character(name, description):
    print(f"Designing character: {name}")
    print(f"Description: {description}")

    # Ensure output directory exists
    output_dir = "output/characters"
    os.makedirs(output_dir, exist_ok=True)

    # Use Pollinations AI (free, no key required) to generate the character
    prompt = f"manga character design, {description}, anime style, high quality, concept art"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

    print("Calling Pollinations.ai API...")
    try:
        response = requests.get(url)
        response.raise_for_status()

        file_path = os.path.join(output_dir, f"{name.lower().replace(' ', '_')}.png")
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Character {name} design completed and saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to generate character: {e}")
        return None

if __name__ == "__main__":
    design_character("Hero", "Brave young male protagonist with spiky black hair, wearing fantasy armor")
