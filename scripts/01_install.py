import os
import shutil

def main():
    print("Starting Manga Automation System installation...")

    # Create directories
    dirs = ['config', 'scripts', 'output', 'characters', 'models', 'docs', 'templates']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Copy env example
    if os.path.exists('config/.env.example') and not os.path.exists('.env'):
        shutil.copy('config/.env.example', '.env')
        print("Copied .env.example to .env")

    print("Installation complete!")

if __name__ == "__main__":
    main()
