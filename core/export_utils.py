import pandas as pd
import openpyxl
import os


def save_entries_to_excel(entries, filename="table_of_contents.xlsx") -> None:
    try:
        df = pd.DataFrame(entries)
        df = df.rename(columns={"title": "Chapter Title", "page": "Page Number"})
        df.to_excel(filename, index=False, engine="openpyxl")

        # Adjust column widths and row heights
        wb = openpyxl.load_workbook(filename)
        ws = wb.active

        if ws is not None:
            ws.column_dimensions['A'].width = 40  # Chapter Title
            ws.column_dimensions['B'].width = 15  # Page Number

            for i in range(2, ws.max_row + 1):
                ws.row_dimensions[i].height = 25

            wb.save(filename)
        print(f"\n✅ Successfully saved to '{filename}'.")
    except Exception as e:
        print("\n❌ Error saving to Excel:", e)
        raise


def convert_to_custom_format(entries) -> str:
    xml_blocks = []
    for item in entries:
        block = f"<anUnit><uTanim>{item['title']}</uTanim><uSayfa>{item['page']}</uSayfa></anUnit>"
        xml_blocks.append(block)
    return "\n".join(xml_blocks)



