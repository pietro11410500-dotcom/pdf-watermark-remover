import streamlit as st
import PyPDF2
import pdf2image
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import os
from pathlib import Path
import tempfile

st.set_page_config(page_title="Watermark Remover", layout="centered")

st.markdown("""
    <style>
    .main { max-width: 800px; margin: 0 auto; }
    .success { color: green; font-weight: bold; }
    .error { color: red; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🔧 PDF Watermark Remover")

if "step" not in st.session_state:
    st.session_state.step = 1
if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None
if "watermark_text" not in st.session_state:
    st.session_state.watermark_text = ""
if "locations" not in st.session_state:
    st.session_state.locations = []
if "processed_pdf" not in st.session_state:
    st.session_state.processed_pdf = None

if st.session_state.step == 1:
    st.subheader("Step 1: Upload PDF File")
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            st.session_state.pdf_file = uploaded_file
            st.success("✅ PDF detected successfully!")
            if st.button("Next"):
                st.session_state.step = 2
                st.rerun()
        else:
            st.error("❌ The file is not a valid PDF!")