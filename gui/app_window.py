import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, StringVar
from ttkbootstrap import Combobox, Window
from tabulate import tabulate
import threading
import os

from config.settings import CONFIG, MODEL_OPTIONS
from core.export_utils import save_entries_to_excel, convert_to_custom_format
from core.gemini_handler import extract_table_of_contents
from core.image_utils import load_images
import google.generativeai as genai


def run_gui():
    root = Window(themename="cyborg")
    root.title("Table of Contents Extractor")
    root.geometry(CONFIG['window_size'])

    selected_model_name = StringVar(master=root, value=MODEL_OPTIONS[0])
    extracted_entries = {"data": []}

    def update_status(text_area, msg):
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, msg + "\n")
        text_area.see(tk.END)
        text_area.config(state=tk.DISABLED)

    def update_entries_display():
        lang = CONFIG['current_language']
        text_area.config(state=tk.NORMAL)
        if extracted_entries["data"]:
            if lang == "tr":
                headers = {"title": "başlık", "page": "sayfa"}
            else:
                headers = {"title": "title", "page": "page"}
            df_text = tabulate(extracted_entries["data"], headers=headers, tablefmt='fancy_grid', showindex=False)
            final_msg = "\n" + CONFIG['languages'][lang]['final_results'] + "\n" + df_text
            text_area.insert(tk.END, final_msg)
        text_area.config(state=tk.DISABLED)

    def on_load_images():
        lang = CONFIG['current_language']
        images = load_images()
        if not images:
            messagebox.showwarning("No Images", "No images were selected or loaded.")
            return

        def task(images):
            try:
                text_area.config(state=tk.NORMAL)
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, CONFIG['languages'][lang]['processing_images'] + "\n")
                text_area.config(state=tk.DISABLED)

                model = genai.GenerativeModel(selected_model_name.get())
                all_entries = extract_table_of_contents(images, model, lambda msg: update_status(text_area, msg))
                all_entries = sorted(all_entries, key=lambda x: x['page'])
                extracted_entries["data"] = all_entries
                update_entries_display()
            except Exception as e:
                root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))
            finally:
                for btn in [btn_load, btn_excel, btn_txt]:
                    btn.config(state=tk.NORMAL)

        for btn in [btn_load, btn_excel, btn_txt]:
            btn.config(state=tk.DISABLED)

        threading.Thread(target=task, args=(images,), daemon=True).start()

    def on_save_excel():
        if not extracted_entries["data"]:
            messagebox.showwarning("No Data", "No data to save. Please load images first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path:
            save_entries_to_excel(extracted_entries["data"], filename=path)
            messagebox.showinfo("Success", f"Saved to {path}")

    def on_save_txt():
        if not extracted_entries["data"]:
            messagebox.showwarning("No Data", "No data to save. Please load images first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            text = convert_to_custom_format(extracted_entries["data"])
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Success", f"Saved to {path}")

    def toggle_language():
        CONFIG['current_language'] = "tr" if CONFIG['current_language'] == "en" else "en"
        lang = CONFIG['current_language']
        btn_load.config(text=CONFIG['languages'][lang]['load_images'])
        btn_excel.config(text=CONFIG['languages'][lang]['save_excel'])
        btn_txt.config(text=CONFIG['languages'][lang]['save_txt'])
        btn_lang.config(text=CONFIG['languages'][lang]['language_toggle'])
        btn_log.config(text=CONFIG['languages'][lang]['view_log'])

    def on_view_log():
        log_path = CONFIG['csv_log_file']
        if not os.path.exists(log_path):
            messagebox.showwarning("Log Not Found", f"Log file '{log_path}' does not exist.")
            return
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        log_window = tk.Toplevel(root)
        log_window.title("Gemini Response Log")
        log_window.geometry("800x600")
        st = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=100, height=40, font=("Consolas", 10))
        st.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        st.insert(tk.END, log_content)
        st.config(state=tk.DISABLED)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    lang = CONFIG['current_language']
    btn_load = tk.Button(btn_frame, text=CONFIG['languages'][lang]['load_images'], command=on_load_images, width=20)
    btn_load.grid(row=0, column=0, padx=10)

    btn_excel = tk.Button(btn_frame, text=CONFIG['languages'][lang]['save_excel'], command=on_save_excel, width=20)
    btn_excel.grid(row=0, column=1, padx=10)

    btn_txt = tk.Button(btn_frame, text=CONFIG['languages'][lang]['save_txt'], command=on_save_txt, width=20)
    btn_txt.grid(row=0, column=2, padx=10)

    btn_lang = tk.Button(btn_frame, text=CONFIG['languages'][lang]['language_toggle'], command=toggle_language, width=20)
    btn_lang.grid(row=0, column=4, padx=10)

    btn_log = tk.Button(btn_frame, text=CONFIG['languages'][lang]['view_log'], command=on_view_log, width=20)
    btn_log.grid(row=0, column=3, padx=10)

    model_combo = Combobox(btn_frame, values=MODEL_OPTIONS, textvariable=selected_model_name, width=25, state="readonly")
    model_combo.grid(row=0, column=5, padx=10)

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=30, font=("Consolas", 10))
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area.config(state=tk.DISABLED)

    root.mainloop()
