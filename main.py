# File: main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from typing import List, Optional
import uuid
import os
import shutil
import tempfile
import base64
import torch
from PIL import Image
from pathlib import Path
from render import render_ocr_text
from globe import ocr_types, ocr_colors, tasks, stop_str, title, description
from transformers import AutoModelForImageTextToText, AutoProcessor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GOT-OCR 2.0 Microservice", 
              description=description,
              version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and processor
model = None
processor = None

@app.on_event("startup")
async def load_model():
    global model, processor
    model_name = "stepfun-ai/GOT-OCR-2.0-hf"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(
        model_name, 
        low_cpu_mem_usage=True,
        device_map=device
    )
    model = model.eval().to(device)

async def cleanup_tempdir(temp_dir: str):
    """Cleanup temporary directory"""
    shutil.rmtree(temp_dir, ignore_errors=True)

def process_image_sync(
    task: str,
    image_paths: List[str],
    temp_dir: str,
    ocr_type: Optional[str] = None,
    ocr_box: Optional[str] = None,
    ocr_color: Optional[str] = None
):
    try:
        images = [Image.open(img_path) for img_path in image_paths]
        unique_id = str(uuid.uuid4())
        result_path = os.path.join(temp_dir, f"{unique_id}.html")
        res = None

        if task == "Plain Text OCR":
            inputs = processor(images, return_tensors="pt").to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            return res, None, unique_id

        elif task == "Format Text OCR":
            inputs = processor(images, return_tensors="pt", format=True).to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            ocr_type = "format"

        elif task == "Fine-grained OCR (Box)":
            if not ocr_box:
                raise ValueError("Bounding box coordinates required")
            try:
                box = list(map(int, ocr_box.strip('[]').split(',')))
                if len(box) != 4:
                    raise ValueError
            except:
                raise ValueError("Invalid box format. Use [x1,y1,x2,y2]")
            
            inputs = processor(images, return_tensors="pt", box=box).to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )

        elif task == "Fine-grained OCR (Color)":
            if not ocr_color or ocr_color not in ocr_colors:
                raise ValueError(f"Invalid color. Choose from {ocr_colors}")
            
            inputs = processor(images, return_tensors="pt", color=ocr_color).to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )

        elif task == "Multi-crop OCR":
            inputs = processor(
                images,
                return_tensors="pt",
                format=True,
                crop_to_patches=True,
                max_patches=5
            ).to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            ocr_type = "format"

        elif task == "Multi-page OCR":
            inputs = processor(
                images,
                return_tensors="pt",
                multi_page=True,
                format=True
            ).to("cuda")
            generate_ids = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings=stop_str,
                max_new_tokens=4096,
            )
            res = processor.decode(
                generate_ids[0, inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )
            ocr_type = "format"

        else:
            raise ValueError(f"Unsupported task: {task}")

        # Handle rendering for formatted outputs
        if any(t in task for t in ["Format", "Fine-grained", "Multi"]):
            render_ocr_text(res, result_path, format_text=ocr_type == "format")
            if os.path.exists(result_path):
                with open(result_path, "r") as f:
                    html_content = f.read()
                return res, html_content, unique_id

        return res, None, unique_id

    except Exception as e:
        raise RuntimeError(f"Processing error: {str(e)}")
    

@app.post("/process", 
          summary="Process OCR request",
          response_description="OCR processing results")
async def process_ocr(
    background_tasks: BackgroundTasks,
    task: str = Form(..., description="OCR task type", example="Plain Text OCR"),
    ocr_type: Optional[str] = Form(None, description="OCR type for formatted output"),
    ocr_box: Optional[str] = Form(None, description="Bounding box coordinates [x1,y1,x2,y2]"),
    ocr_color: Optional[str] = Form(None, description="Highlight color for regions"),
    images: List[UploadFile] = File(..., description="Input images for processing")
):
    """Main OCR processing endpoint supporting all GOT-OCR 2.0 features"""
    
    # Validate input
    if task not in tasks:
        raise HTTPException(400, detail="Invalid task specified")
    
    if task == "Fine-grained OCR (Color)" and ocr_color not in ocr_colors:
        raise HTTPException(400, detail="Invalid color specified")
    
    if task == "Fine-grained OCR (Box)" and not ocr_box:
        raise HTTPException(400, detail="Missing bounding box coordinates")

    # Create temporary workspace
    temp_dir = tempfile.mkdtemp()
    background_tasks.add_task(cleanup_tempdir, temp_dir)

    # Save uploaded images
    img_paths = []
    for img in images:
        if not img.content_type.startswith("image/"):
            raise HTTPException(400, detail="Invalid file type uploaded")
        
        img_path = os.path.join(temp_dir, img.filename)
        with open(img_path, "wb") as buffer:
            content = await img.read()
            buffer.write(content)
        img_paths.append(img_path)

    # Process images
    try:
        text_result, html_content, result_id = await run_in_threadpool(
            process_image_sync,
            task=task,
            image_paths=img_paths,
            temp_dir=temp_dir,
            ocr_type=ocr_type,
            ocr_box=ocr_box,
            ocr_color=ocr_color
        )
    except Exception as e:
        raise HTTPException(500, detail=str(e))

    # Prepare response
    response = {
        "result_id": result_id,
        "text": text_result,
        "html_available": False
    }

    if html_content:
        encoded_html = base64.b64encode(html_content.encode()).decode()
        response.update({
            "html": encoded_html,
            "html_available": True,
            "download_url": f"/results/{result_id}"
        })

    return JSONResponse(content=response)

@app.get("/results/{result_id}", 
         summary="Retrieve processed results",
         response_description="HTML content of processed result")
async def get_result(result_id: str):
    """Retrieve HTML-rendered results by ID"""
    # Implement result storage/retrieval logic here
    return JSONResponse(content={"detail": "Result storage not implemented"}, status_code=501)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)