import os
from PIL import Image

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def compile_pdf(output_filename, input_dir):
    print(f"Compiling PDF from images in {input_dir}...")

    # Create output dir if it doesn't exist
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    # Look in the processed directory first, then the base pages directory
    processed_dir = os.path.join(input_dir, "processed")
    target_dir = processed_dir if os.path.exists(processed_dir) and os.listdir(processed_dir) else input_dir

    images = [f for f in os.listdir(target_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()

    if not images:
        print(f"No images found in {target_dir} to compile.")
        return

    if not REPORTLAB_AVAILABLE:
        print("ReportLab is not installed. Using PIL to save PDF...")
        try:
            img_list = []
            for img_name in images:
                img_path = os.path.join(target_dir, img_name)
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img_list.append(img)

            if img_list:
                img_list[0].save(output_filename, save_all=True, append_images=img_list[1:])
                print(f"PDF compiled and saved to {output_filename}")
        except Exception as e:
            print(f"Error saving PDF with PIL: {e}")
        return

    try:
        c = canvas.Canvas(output_filename, pagesize=letter)
        page_width, page_height = letter

        for img_name in images:
            img_path = os.path.join(target_dir, img_name)
            # We want to fill the page while maintaining aspect ratio, or simply stretch to fit
            # For simplicity, let's stretch to fit the letter size
            c.drawImage(img_path, 0, 0, width=page_width, height=page_height)
            c.showPage()

        c.save()
        print(f"Real PDF compiled and saved to {output_filename}")
    except Exception as e:
        print(f"Error creating PDF with ReportLab: {e}")

if __name__ == "__main__":
    compile_pdf("output/manga.pdf", "./output/pages")
