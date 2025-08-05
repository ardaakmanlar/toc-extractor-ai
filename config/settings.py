CONFIG = {
    'csv_log_file': 'gemini_response_log.csv',
    'model_name': 'gemini-2.0-flash-lite',
    'window_size': '1400x1000',
    'languages': {
        "en": {
            "load_images": "Load Images",
            "save_excel": "Save as Excel", 
            "save_txt": "Save as TXT",
            "view_log": "View Log",
            "language_toggle": "Türkçe",
            'processing_images': 'Processing images, please wait...',
            'gemini_processing': 'Gemini is processing...',
            'processing_image': 'Processing image {idx}/{total}: Sending to Gemini...',
            'extracted_entries': 'Image {idx}: Extracted {count} entries',
            'final_results': '='*50+'RESULTS'+'='*50,
            'no_entries': 'No entries extracted.'
        },
        "tr": {
            "load_images": "Resimleri Yükle",
            "save_excel": "Excel Olarak Kaydet",
            "save_txt": "TXT Olarak Kaydet", 
            "view_log": "Logu Görüntüle",
            "language_toggle": "English",
            'processing_images': 'Resimler işleniyor, lütfen bekleyin...',
            'gemini_processing': 'Gemini işleniyor...',
            'processing_image': 'Resim {idx}/{total} işleniyor: Gemini\'ye gönderiliyor...',
            'extracted_entries': 'Resim {idx}: {count} başlık çıkarıldı',
            'final_results': '='*50+'SONUÇLAR'+'='*50,
            'no_entries': 'Hiç başlık çıkarılamadı.'
        }
    },
    'current_language': 'en',
    "prompt": (
    "You are given a high-resolution image of a book's Table of Contents.\n\n"
    "Your task is to extract **every visible line** that includes a title and a page number.\n\n"
    "This includes:\n"
    "- Main headings (like \"Bölüm\", \"Tema\", \"Cevap Anahtarı\")\n"
    "- Sub-sections like \"Bilgi Alanı - Keşfetme Alanı\", \"Kontrol Alanı\", etc.\n\n"
    "Very important:\n"
    "- Lines like “Bilgi Alanı - Keşfetme Alanı ..... 6-11” must be processed.\n"
    "- From any range like 6-11, extract only the **first number** (e.g., 6).\n"
    "- If a line has **no page number**, assume it shares the **same page number** as the line below it that has a valid page number.\n"
    "- Return every valid line, even if the format varies.\n"
    "- Work **line by line**, do not skip any section.\n\n"
    "Output format (strictly one entry per line):\n"
    "<Title> - <Page Number>\n\n"
    "Do not include any extra explanation, quotes, or formatting. Just plain lines.\n\n"
    "Examples:\n"
    "1. Günlük Hayatta Kimya - 6\n"
    "Bilgi Alanı - Keşfetme Alanı - 6\n"
    "Kontrol Alanı 1 - 2 - 12"
    ),
}

MODEL_OPTIONS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]
