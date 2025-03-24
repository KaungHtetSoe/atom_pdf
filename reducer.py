# reducer.py

import fitz  # PyMuPDF
from PIL import Image
import io

def reduce_pdf(input_path, output_path, quality=50):
    original_pdf = fitz.open(input_path)
    new_pdf = fitz.open()

    for page_num in range(len(original_pdf)):
        page = original_pdf.load_page(page_num)
        pix = page.get_pixmap(dpi=96)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="JPEG", quality=quality)
        img_byte_arr.seek(0)

        img_rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = new_pdf.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(img_rect, stream=img_byte_arr.read())

    new_pdf.save(output_path)
    original_pdf.close()
    new_pdf.close()
    print(f"✅ PDF reduced and saved to: {output_path}")

