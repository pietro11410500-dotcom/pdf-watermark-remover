import streamlit as st
import PyPDF2

def remove_watermark(pdf_file, watermark_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    watermark_reader = PyPDF2.PdfReader(watermark_file)
    output_pdf = PyPDF2.PdfWriter()

    for page in range(len(pdf_reader)):
        pdf_page = pdf_reader.pages[page]
        watermark_page = watermark_reader.pages[0]

        # Merge the watermark with the current page
        pdf_page.merge_page(watermark_page)
        output_pdf.add_page(pdf_page)

    output_file = "output.pdf"
    with open(output_file, "wb") as f:
        output_pdf.write(f)

    return output_file

st.title("PDF Watermark Remover")

uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
uploaded_watermark = st.file_uploader("Choose a watermark file", type="pdf")

if st.button("Remove Watermark"):
    if uploaded_pdf and uploaded_watermark:
        output_file = remove_watermark(uploaded_pdf, uploaded_watermark)
        st.success(f"Watermark removed! Download it [here](./{output_file})")
    else:
        st.error("Please upload both PDF and watermark files."),
