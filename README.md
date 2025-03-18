# GOT-OCR 2.0 Microservice 🚀

State-of-the-art OCR microservice powered by Transformers and FastAPI, supporting multiple OCR tasks and formats.

## 📌 Key Features

- **Multi-Task OCR Support**
  - Plain Text Extraction
  - Formatted Text (LaTeX/Markdown)
  - Region-Specific OCR (Box/Color)
  - Multi-Page Document Processing
  - Sheet Music & Math Formula Recognition
- **Input Formats**: JPEG, PNG, TIFF
- **Output Formats**: Raw Text, HTML, SVG
- **GPU Acceleration** Support (CUDA)

## 🛠 Installation

### Prerequisites
- Python 3.9+
- CUDA 11.7+ (For GPU acceleration)
- Docker 20.10+ (Optional)

### Without Docker
```bash
# Clone repository
git clone https://github.com/iammuhammadnoumankhan/FastAPI-GOT-OCR-2-Transformers.git
cd got-ocr-service

# Install dependencies
pip install -r requirements.txt

# Start service (CPU)
uvicorn main:app --host 0.0.0.0 --port 8000

# Start with GPU
CUDA_VISIBLE_DEVICES=0 uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Docker
```bash
# Build the Docker image:
docker build -t got-ocr-service .

# Run the container:
docker run -p 8000:8000 --gpus all got-ocr-service
```

## 🚀 Usage

### Supported Tasks

| Task | Parameters | Description |
|------|------------|-------------|
| `Plain Text OCR` | None | Basic text extraction |
| `Format Text OCR` | `ocr_type=format` | Structured text output |
| `Fine-grained OCR (Box)` | `ocr_box=[x1,y1,x2,y2]` | Region-specific extraction |
| `Fine-grained OCR (Color)` | `ocr_color=red/green/blue` | Color-based extraction |
| `Multi-crop OCR` | None | Multiple region processing |
| `Multi-page OCR` | Multiple images | Document processing |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process` | POST | Main OCR processing |
| `/results/{result_id}` | GET | Retrieve HTML results |
| `/docs` | GET | Interactive API documentation |

## 📋 Example Requests

### 1. Basic Text Extraction
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Plain Text OCR" \
  -F "images=@document.jpg"
```

### 2. Math Formula Recognition
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Format Text OCR" \
  -F "ocr_type=format" \
  -F "images=@equation.png"
```

### 3. Multi-Page Processing
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Multi-page OCR" \
  -F "images=@page1.pdf" \
  -F "images=@page2.pdf"
```

### 4. Color-Based Extraction
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Fine-grained OCR (Color)" \
  -F "ocr_color=red" \
  -F "images=@highlighted_text.png"
```

## 📚 API Documentation

Interactive Swagger documentation available at:
`http://localhost:8000/docs`


### Build & Run
```bash
# Build the Docker image:
docker build -t got-ocr-service .

# Run the container:
docker run -p 8000:8000 --gpus all got-ocr-service
```

## 📜 License

APACHE 2.0 License 

---

**Note**: Replace `localhost:8000` with your domain in production deployments. For large-scale usage, consider adding:
- Redis caching
- Load balancing
- Rate limiting
``` 

```

## More CURLs Commands:

Here are the `curl` commands for all the supported use cases and types in the GOT-OCR 2.0 FastAPI microservice:

---

### **1. Plain Text OCR**
Extracts plain text from an image.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Plain Text OCR" \
  -F "images=@document.jpg"
```

---

### **2. Formatted Text OCR**
Extracts formatted text (e.g., LaTeX, Markdown) from an image.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Format Text OCR" \
  -F "ocr_type=format" \
  -F "images=@formatted_document.png"
```

---

### **3. Fine-grained OCR (Box)**
Extracts text from a specific bounding box region in the image.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Fine-grained OCR (Box)" \
  -F "ocr_box=[100,100,300,300]" \
  -F "images=@image_with_regions.jpg"
```

---

### **4. Fine-grained OCR (Color)**
Extracts text from regions highlighted with a specific color.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Fine-grained OCR (Color)" \
  -F "ocr_color=red" \
  -F "images=@color_highlighted_image.png"
```

---

### **5. Multi-crop OCR**
Processes multiple cropped regions of an image.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Multi-crop OCR" \
  -F "images=@multi_crop_image.jpg"
```

---

### **6. Multi-page OCR**
Processes multiple pages of a document.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Multi-page OCR" \
  -F "images=@page1.png" \
  -F "images=@page2.png" \
  -F "images=@page3.png"
```

---

### **7. Sheet Music OCR**
Processes sheet music and generates formatted output.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Format Text OCR" \
  -F "ocr_type=format" \
  -F "images=@sheet_music.png"
```

---

### **8. Math Formula OCR**
Extracts mathematical formulas from an image.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Format Text OCR" \
  -F "ocr_type=format" \
  -F "images=@math_formula.png"
```

---

### **9. Table and Chart OCR**
Extracts structured data from tables and charts.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Format Text OCR" \
  -F "ocr_type=format" \
  -F "images=@table_chart.png"
```

---

### **10. Batch Processing**
Process multiple images in a single request.

```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Plain Text OCR" \
  -F "images=@image1.jpg" \
  -F "images=@image2.png" \
  -F "images=@image3.tiff"
```

---

### **11. Retrieve HTML Results**
After processing, retrieve the HTML-rendered result using the `result_id`.

```bash
curl -X GET "http://localhost:8000/results/{result_id}"
```

Replace `{result_id}` with the ID returned in the response from the `/process` endpoint.

---

### **12. Error Handling Examples**
#### Missing Image
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Plain Text OCR"
```
Response:
```json
{
  "detail": "No image provided"
}
```

#### Invalid Task
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Invalid Task" \
  -F "images=@document.jpg"
```
Response:
```json
{
  "detail": "Invalid task specified"
}
```

#### Invalid Color
```bash
curl -X POST "http://localhost:8000/process" \
  -F "task=Fine-grained OCR (Color)" \
  -F "ocr_color=purple" \
  -F "images=@image.jpg"
```
Response:
```json
{
  "detail": "Invalid color specified"
}
```

---

### **Notes**:
1. Replace `http://localhost:8000` with your actual server URL if deployed elsewhere.
2. Ensure the image files (`@document.jpg`, `@formatted_document.png`, etc.) exist in the directory where you run the `curl` command.
3. For multi-file uploads, use multiple `-F "images=@file"` fields.
4. The `ocr_box` parameter should be in the format `[x1,y1,x2,y2]`.
5. The `ocr_color` parameter supports only `red`, `green`, or `blue`.

These commands cover all the supported use cases and types for the GOT-OCR 2.0 microservice.
