import time
import csv
from datetime import datetime
from typing import List, Dict
from PIL import Image
import google.generativeai as genai
from core.image_utils import preprocess_image
from config.settings import CONFIG
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def parse_line_based_output(text: str) -> List[Dict[str, int]]:
    entries = []
    lines = text.strip().split("\n")

    for line in lines:
        if "-" not in line:
            continue
        try:
            title_part, page_part = line.rsplit("-", 1)
            title = title_part.strip()
            page = int(page_part.strip())
            entries.append({"title": title, "page": page})
        except Exception as e:
            print("Line parsing failed:", line)
            print("Error:", e)
            continue
    return entries


def extract_table_of_contents(images: List[Image.Image], model, update_callback=None) -> List[Dict[str, int]]:
    prompt = CONFIG['prompt']
    all_entries = []

    for idx, img in enumerate(images):
        try:
            if update_callback:
                update_callback(f"Image {idx+1}/{len(images)}: Sending to Gemini...")

            start_time = time.time()
            response = model.generate_content([prompt, preprocess_image(img)])
            elapsed = time.time() - start_time

            # Log response time
            model_name = getattr(model, 'model_name', getattr(model, '_model_name', 'unknown_model'))
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(CONFIG['csv_log_file'], 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, model_name, f"{elapsed:.2f}"])

            entries = parse_line_based_output(response.text)
            all_entries.extend(entries)

            if update_callback:
                update_callback(f"Image {idx+1}: Extracted {len(entries)} entries")

        except Exception as e:
            print(f"Error processing image {idx+1}: {e}")
            continue

    return all_entries


def initialize_gemini():
    return genai.GenerativeModel(CONFIG['model_name'])
