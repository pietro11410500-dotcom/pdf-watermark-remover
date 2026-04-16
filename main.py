import streamlit as st
import pdf2image
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import subprocess
import sys

# Auto-instala dependências
try:
    import pdf2image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdf2image", "pillow", "opencv-python", "numpy"])

st.set_page_config(page_title="🔧 PDF Watermark Remover", layout="wide")

st.markdown("""
    <style>
    .main { max-width: 1000px; margin: 0 auto; }
    .stButton>button { width: 100%; padding: 10px; font-size: 16px; }
    h1 { color: #FF6B6B; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🔧 PDF Watermark Remover")
st.markdown("---")

# Session state
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

def remove_watermark(image, watermark_text, locations):
    result = image.copy()
    
    if len(result.shape) == 3:
        gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    else:
        gray = result
    
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    h, w = result.shape[:2]
    
    for contour in contours:
        x, y, cw, ch = cv2.boundingRect(contour)
        center_x = x + cw / 2
        center_y = y + ch / 2
        
        margin = 0.2
        is_top = center_y < h * margin
        is_bottom = center_y > h * (1 - margin)
        is_left = center_x < w * margin
        is_right = center_x > w * (1 - margin)
        
        is_watermark = False
        if "Variado" in locations:
            is_watermark = True
        else:
            if "Topo" in locations and is_top:
                is_watermark = True
            if "Fundo" in locations and is_bottom:
                is_watermark = True
            if "Esquerda" in locations and is_left:
                is_watermark = True
            if "Direita" in locations and is_right:
                is_watermark = True
        
        if is_watermark:
            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            
            if len(result.shape) == 3:
                result = cv2.inpaint(result, mask, 3, cv2.INPAINT_TELEA)
            else:
                result_3ch = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
                result_3ch = cv2.inpaint(result_3ch, mask, 3, cv2.INPAINT_TELEA)
                result = cv2.cvtColor(result_3ch, cv2.COLOR_RGB2GRAY)
    
    result = cv2.bilateralFilter(result, 9, 75, 75)
    return result

def repair_image(image):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Sharpness(pil_image)
    pil_image = enhancer.enhance(0.9)
    pil_image = pil_image.filter(ImageFilter.MedianFilter(size=3))
    return np.array(pil_image)

# STEP 1: Upload
if st.session_state.step == 1:
    st.subheader("📄 Step 1: Upload PDF")
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])
    
    if uploaded_file:
        st.session_state.pdf_file = uploaded_file
        st.success("✅ PDF detected!")
        
        if st.button("➡️ Next"):
            st.session_state.step = 2
            st.rerun()

# STEP 2: Watermark Text
elif st.session_state.step == 2:
    st.subheader("📝 Step 2: Watermark Text")
    st.info(f"📄 File: {st.session_state.pdf_file.name}")
    
    watermark_input = st.text_input(
        "Enter watermark text:",
        placeholder="Ex: PIETRO SILVA (15073190)"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("➡️ Next"):
            if watermark_input.strip():
                st.session_state.watermark_text = watermark_input
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Enter the watermark text!")

# STEP 3: Locations
elif st.session_state.step == 3:
    st.subheader("📍 Step 3: Watermark Locations")
    st.info(f"📝 Watermark: {st.session_state.watermark_text}")
    
    col1, col2 = st.columns(2)
    with col1:
        topo = st.checkbox("Topo (Top)")
        fundo = st.checkbox("Fundo (Bottom)")
    with col2:
        esquerda = st.checkbox("Esquerda (Left)")
        direita = st.checkbox("Direita (Right)")
    
    st.markdown("---")
    variado = st.checkbox("✓ Variado/Aleatório")
    
    locations = []
    if topo:
        locations.append("Topo")
    if fundo:
        locations.append("Fundo")
    if esquerda:
        locations.append("Esquerda")
    if direita:
        locations.append("Direita")
    if variado:
        locations.append("Variado")
    
    st.session_state.locations = locations if locations else ["Variado"]
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("➡️ Process"):
            if st.session_state.locations:
                st.session_state.step = 4
                st.rerun()

# STEP 4: Processing
elif st.session_state.step == 4:
    st.subheader("⏳ Processing...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📥 Converting PDF to images...")
        pdf_bytes = st.session_state.pdf_file.read()
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=150)
        
        total_pages = len(images)
        processed_images = []
        
        for idx, image in enumerate(images):
            progress = int((idx / total_pages) * 100)
            progress_bar.progress(progress)
            status_text.text(f"🔄 Page {idx + 1}/{total_pages}...")
            
            img_array = np.array(image)
            processed = remove_watermark(img_array, st.session_state.watermark_text, st.session_state.locations)
            repaired = repair_image(processed)
            processed_images.append(Image.fromarray(repaired))
        
        status_text.text("📤 Generating PDF...")
        output_pdf = io.BytesIO()
        processed_images[0].save(
            output_pdf,
            format="PDF",
            save_all=True,
            append_images=processed_images[1:],
            quality=95
        )
        output_pdf.seek(0)
        
        st.session_state.processed_pdf = output_pdf
        progress_bar.progress(100)
        status_text.text("✅ Done!")
        
        st.session_state.step = 5
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# STEP 5: Download
elif st.session_state.step == 5:
    st.success("✅ Watermark removed successfully!")
    
    filename = "Aprender ja - MG - 8 ano - Lingua portuguesa - Caderno 1.pdf"
    
    st.download_button(
        label="📥 Download Cleaned PDF",
        data=st.session_state.processed_pdf,
        file_name=filename,
        mime="application/pdf"
    )
    
    st.markdown("---")
    if st.button("✓ Process Another File"):
        st.session_state.step = 1
        st.session_state.pdf_file = None
        st.session_state.watermark_text = ""
        st.session_state.locations = []
        st.session_state.processed_pdf = None
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>❤️ Made by Pietro Silva</div>", unsafe_allow_html=True)
