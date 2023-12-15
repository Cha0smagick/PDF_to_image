import streamlit as st
import fitz
from PIL import Image
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

        export_format = st.selectbox("Select export format", ["JPEG", "PNG"])

        # Display the first page initially
        first_page = images[0]
        st.image(first_page, caption="Page 1", use_column_width=True)

        # Container for the rest of the pages
        container = st.container()

        # Add the rest of the pages to the container
        for i, img in enumerate(images[1:]):
            container.image(img, caption=f"Page {i + 2}", use_column_width=True)

        # Download button for the currently displayed page
        current_page = st.slider("Select Page", 1, len(images), 1)
        img_format = export_format.lower()
        img_bytes = BytesIO()
        images[current_page - 1].save(img_bytes, format=img_format)

        st.download_button(
            label=f"Download Page {current_page} as {export_format}",
            data=img_bytes.getvalue(),
            file_name=f"page_{current_page}.{img_format}",
            key=f"download_button_{current_page}",
        )

if __name__ == "__main__":
    main()
