import fitz  # PyMuPDF
from PIL import Image
import io

def estimate_compressed_size(input_path, dpi=96, quality=30, grayscale=False):
    doc = fitz.open(input_path)
    estimated_total = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if grayscale:
            img = img.convert("L")

        img_io = io.BytesIO()
        img.save(img_io, format="JPEG", quality=quality, optimize=True)
        estimated_total += len(img_io.getvalue())

    doc.close()
    return round(estimated_total / 1024 / 1024, 2)  # return MB

def reduce_pdf(input_path, output_path, dpi=96, quality=30, grayscale=False):
    original_pdf = fitz.open(input_path)
    new_pdf = fitz.open()

    for page_num in range(len(original_pdf)):
        page = original_pdf.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if grayscale:
            img = img.convert("L")

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="JPEG", quality=quality, optimize=True)
        img_byte_arr.seek(0)

        img_rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = new_pdf.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(img_rect, stream=img_byte_arr.read())

    new_pdf.save(output_path)
    original_pdf.close()
    new_pdf.close()