# PDF Watermark Remover 🔧

A powerful, user-friendly web application built with Streamlit that removes watermarks from PDF files while preserving the original document quality and repairing any damage caused by the removal process.

## Features ✨

- 🎯 **Smart Watermark Detection** - Automatically detects and removes watermarks from specific locations
- 🎨 **Image Repair** - Repairs potential damage caused by watermark removal
- 📊 **Progress Tracking** - Real-time progress bar showing processing status
- 🌐 **Web-Based Interface** - No installation needed, runs in your browser
- ♿ **User-Friendly** - Intuitive step-by-step wizard interface
- 🔒 **Local Processing** - All processing happens locally on your machine
- 📥 **Easy Download** - Download your cleaned PDF with a single click

## Prerequisites 📋

- Python 3.8 or higher
- pip (Python package manager)
- Poppler (for PDF to image conversion)

### Installing Poppler

**Windows:**
```bash
# Using Chocolatey
choco install poppler

# Or download from: https://github.com/oschwartz10612/poppler-windows/releases
```

**macOS:**
```bash
brew install poppler
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install poppler-utils
```

**Linux (Fedora/CentOS):**
```bash
sudo yum install poppler-utils
```

## Installation 🚀

1. **Clone the repository:**
```bash
git clone https://github.com/pietro11410500-dotcom/pdf-watermark-remover.git
cd pdf-watermark-remover
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage 🎯

1. **Start the application:**
```bash
streamlit run main.py
```

2. **Open your browser** and navigate to:
```
http://localhost:8501
```

3. **Follow the wizard steps:**
   - **Step 1:** Upload your PDF file
   - **Step 2:** Enter the watermark text (e.g., "CONFIDENTIAL")
   - **Step 3:** Select watermark locations (Top, Bottom, Left, Right, or Random)
   - **Step 4:** Wait for processing (progress bar shows real-time status)
   - **Step 5:** Download your cleaned PDF

## How It Works 🔍

The application uses advanced image processing techniques:

1. **PDF Conversion** - Converts PDF pages to high-quality images (300 DPI)
2. **Watermark Detection** - Uses OpenCV to detect text/watermarks in specified locations
3. **Intelligent Removal** - Applies inpainting algorithms (TELEA) to remove watermarks
4. **Image Repair** - Enhances contrast and sharpness to repair any damage
5. **PDF Reconstruction** - Combines processed images back into a PDF file

## Dependencies 📦

- **streamlit** - Web app framework
- **PyPDF2** - PDF manipulation
- **pdf2image** - PDF to image conversion
- **opencv-python** - Computer vision and image processing
- **pillow** - Image processing
- **numpy** - Numerical computing

See `requirements.txt` for version details.

## Configuration ⚙️

You can customize the application by editing `main.py`:

- **DPI:** Change `dpi=300` for higher/lower quality
- **Inpainting:** Modify `cv2.INPAINT_TELEA` to `cv2.INPAINT_NS` for different algorithms
- **Margin:** Adjust `margin = 0.2` to change watermark detection radius
- **Bilateral Filter:** Modify `cv2.bilateralFilter(result, 9, 75, 75)` parameters for different smoothing effects

## Troubleshooting 🐛

**Issue: "Poppler is not installed"**
- Solution: Install Poppler following the Prerequisites section

**Issue: "Module not found"**
- Solution: Ensure you're in the virtual environment and have run `pip install -r requirements.txt`

**Issue: "Watermark not completely removed"**
- Solution: Try selecting "Random" location option or ensure you entered the correct watermark text

**Issue: "Image quality degraded"**
- Solution: Increase DPI value or adjust the repair filter parameters in code

## Advanced Usage 🎓

### Batch Processing (Manual)

To process multiple PDFs, simply run the application multiple times and process each file individually.

### Custom Watermark Patterns

The application detects watermarks based on:
- Text content (exact match)
- Location on page (Top, Bottom, Left, Right, Random)
- Visual characteristics (lighter than main content)

### Performance Tips

- For large PDFs: Process in batches or increase system RAM
- For faster processing: Reduce DPI (trade-off with quality)
- Use SSD storage for faster I/O operations

## Limitations ⚠️

- Works best with text-based watermarks
- Complex graphical watermarks may require multiple passes
- Very faint watermarks might not be detected
- Image quality depends on original PDF resolution

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs by creating an issue
- Suggest features via pull requests
- Improve documentation

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting-🐛) section
2. Review existing [GitHub Issues](https://github.com/pietro11410500-dotcom/pdf-watermark-remover/issues)
3. Create a new issue with detailed description

## Disclaimer ⚖️

This tool is provided for legitimate purposes only. Users are responsible for ensuring they have the right to remove watermarks from documents they process. Always respect copyright and intellectual property rights.

## Author 👤

Created by **Pietro Silva**

---

**Made with ❤️ for document processing**