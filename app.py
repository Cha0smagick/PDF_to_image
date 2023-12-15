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

        # Dropdown menu for selecting export format
        export_format = st.selectbox("Select Export Format", ["JPEG", "PNG"])

        # Dropdown menu for selecting page
        selected_page = st.selectbox("Select Page", range(1, len(images) + 1))

        # Display PDF page using Markdown
        img_format = export_format.lower()
        img_bytes = BytesIO()
        images[selected_page - 1].save(img_bytes, format=img_format)
        base64_img = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
        markdown_img = f'<img src="data:image/{img_format};base64,{base64_img}" alt="Page {selected_page}" style="max-width: 100%;">'
        st.markdown(markdown_img, unsafe_allow_html=True)

        # Download button for the currently displayed page
        img_bytes_download = BytesIO()
        images[selected_page - 1].save(img_bytes_download, format=img_format)

        st.download_button(
            label=f"Download Page {selected_page} as {export_format}",
            data=img_bytes_download.getvalue(),
            file_name=f"page_{selected_page}.{export_format.lower()}",
            key=f"download_button_{selected_page}_{export_format}",
        )

if __name__ == "__main__":
    main()
