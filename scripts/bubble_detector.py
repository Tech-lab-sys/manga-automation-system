import os
import cv2
import numpy as np

def detect_bubbles(input_dir):
    print(f"Loading basic computer vision for speech bubble detection...")
    print(f"Scanning pages in {input_dir}...")

    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    pages = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not pages:
        print("No images found to process.")
        return

    # Ensure output directory for processed images
    output_dir = os.path.join(input_dir, "processed")
    os.makedirs(output_dir, exist_ok=True)

    for page in pages:
        print(f"Processing {page}...")
        img_path = os.path.join(input_dir, page)

        try:
            # Read image
            img = cv2.imread(img_path)
            if img is None:
                continue

            # Basic bubble detection logic (finding white regions)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Threshold to find white areas (potential bubbles)
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            bubble_count = 0
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # Filter by area to avoid noise
                if area > 1000 and area < 50000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    # Draw rectangle around detected bubble
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    # Add mock text
                    cv2.putText(img, "Text", (x+10, y+h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                    bubble_count += 1

            out_path = os.path.join(output_dir, page)
            cv2.imwrite(out_path, img)
            print(f"Found {bubble_count} potential bubbles. Saved to {out_path}")

        except Exception as e:
            print(f"Error processing {page}: {e}")

    print("Bubble detection and text placement complete.")

if __name__ == "__main__":
    detect_bubbles("./output/pages")
