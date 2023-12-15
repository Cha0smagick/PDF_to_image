import streamlit as st
import fitz
from PIL import Image
import base64
from io import BytesIO

def pdf_to_images(pdf_bytes):
    doc = fitz.open("pdf", pdf_bytes)
    images = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        image = page.get_pixmap()
        img = Image.frombytes("RGB", [image.width, image.height], image.samples)
        images.append(img)

    return images

def main():
    st.title("PDF to Image Converter")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF file uploaded successfully!")

        # Read PDF file as bytes
        pdf_bytes = uploaded_file.read()

        images = pdf_to_images(pdf_bytes)

        # Slider for both navigating through pages and selecting export format
        current_page_and_format = st.slider(
            "Select Page and Export Format",
            min_value=1,
            max_value=len(images),
            value=(1, 1),  # Default: First page and first format
            step=1
        )

        current_page, export_format_index = current_page_and_format

        export_format_options = ["JPEG", "PNG"]
        export_format = export_format_options[export_format_index - 1]

        # Display PDF pages horizontally using iframe
        pdf_display = '<div style="overflow-x: scroll; white-space: nowrap;">'
        for i, img in enumerate(images):
            img_format = export_format.lower()
            img_bytes = BytesIO()
            img.save(img_bytes, format=img_format)
            base64_img = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
            pdf_display += f'<img src="data:image/{img_format};base64,{base64_img}" alt="Page {i + 1}" style="max-width: 100%; margin-right: 10px;">'

        pdf_display += '</div>'
        st.markdown(pdf_display, unsafe_allow_html=True)

        # Download button for the currently displayed page
        img_bytes = BytesIO()
        images[current_page - 1].save(img_bytes, format=export_format)

        st.download_button(
            label=f"Download Page {current_page} as {export_format}",
            data=img_bytes.getvalue(),
            file_name=f"page_{current_page}.{export_format.lower()}",
            key=f"download_button_{current_page}_{export_format}",
        )

if __name__ == "__main__":
    main()
