import requests
import os
import json
import base64
from pathlib import Path
import time

# Configuration
API_URL = "http://localhost:8000"
PROCESS_ENDPOINT = f"{API_URL}/process"
RESULTS_ENDPOINT = f"{API_URL}/results"
TEST_IMAGES_DIR = "example-img"  # Directory containing test images

# Ensure the test images directory exists
if not os.path.exists(TEST_IMAGES_DIR):
    os.makedirs(TEST_IMAGES_DIR)
    print(f"Created directory {TEST_IMAGES_DIR}. Please add test images to this directory.")
    exit(1)

# Create output directory for results
OUTPUT_DIR = "test_results"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def test_plain_text_ocr():
    """Test Plain Text OCR functionality"""
    print("\n=== Testing Plain Text OCR ===")
    
    # Get the first image in the test directory
    image_path = next(Path(TEST_IMAGES_DIR).glob("*.*"))
    
    files = {
        'images': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }
    
    data = {
        'task': 'Plain Text OCR'
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the result to a file
        with open(os.path.join(OUTPUT_DIR, "plain_text_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_format_text_ocr():
    """Test Format Text OCR functionality"""
    print("\n=== Testing Format Text OCR ===")
    
    # Get the first image in the test directory
    image_path = next(Path(TEST_IMAGES_DIR).glob("*.*"))
    
    files = {
        'images': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }
    
    data = {
        'task': 'Format Text OCR',
        'ocr_type': 'format'
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the text result
        with open(os.path.join(OUTPUT_DIR, "format_text_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        # Save HTML if available
        if result.get('html_available'):
            html_content = base64.b64decode(result.get('html')).decode('utf-8')
            with open(os.path.join(OUTPUT_DIR, "format_text_result.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML output saved.")
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_box_ocr():
    """Test Fine-grained OCR (Box) functionality"""
    print("\n=== Testing Fine-grained OCR (Box) ===")
    
    # Get the first image in the test directory
    image_path = next(Path(TEST_IMAGES_DIR).glob("*.*"))
    
    files = {
        'images': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }
    
    # Using a sample box - adjust coordinates based on your test image
    data = {
        'task': 'Fine-grained OCR (Box)',
        'ocr_box': '[100,100,300,300]'
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the result
        with open(os.path.join(OUTPUT_DIR, "box_ocr_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_color_ocr():
    """Test Fine-grained OCR (Color) functionality"""
    print("\n=== Testing Fine-grained OCR (Color) ===")
    
    # Get the first image in the test directory
    image_path = next(Path(TEST_IMAGES_DIR).glob("*.*"))
    
    files = {
        'images': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }
    
    data = {
        'task': 'Fine-grained OCR (Color)',
        'ocr_color': 'red'  # Test with red color
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the result
        with open(os.path.join(OUTPUT_DIR, "color_ocr_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_multi_crop_ocr():
    """Test Multi-crop OCR functionality"""
    print("\n=== Testing Multi-crop OCR ===")
    
    # Get the first image in the test directory
    image_path = next(Path(TEST_IMAGES_DIR).glob("*.*"))
    
    files = {
        'images': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }
    
    data = {
        'task': 'Multi-crop OCR'
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the text result
        with open(os.path.join(OUTPUT_DIR, "multi_crop_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        # Save HTML if available
        if result.get('html_available'):
            html_content = base64.b64decode(result.get('html')).decode('utf-8')
            with open(os.path.join(OUTPUT_DIR, "multi_crop_result.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML output saved.")
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_multi_page_ocr():
    """Test Multi-page OCR functionality"""
    print("\n=== Testing Multi-page OCR ===")
    
    # Get up to 3 images from the test directory
    image_paths = list(Path(TEST_IMAGES_DIR).glob("*.*"))[:3]
    
    if len(image_paths) < 2:
        print("Warning: Multi-page OCR test requires at least 2 images. Using available images.")
    
    files = []
    for img_path in image_paths:
        files.append(('images', (os.path.basename(img_path), open(img_path, 'rb'), 'image/jpeg')))
    
    data = {
        'task': 'Multi-page OCR'
    }
    
    response = requests.post(PROCESS_ENDPOINT, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Result ID: {result.get('result_id')}")
        print(f"Extracted Text: {result.get('text')[:100]}...")  # Show first 100 chars
        
        # Save the text result
        with open(os.path.join(OUTPUT_DIR, "multi_page_result.txt"), "w", encoding="utf-8") as f:
            f.write(result.get('text', ''))
        
        # Save HTML if available
        if result.get('html_available'):
            html_content = base64.b64decode(result.get('html')).decode('utf-8')
            with open(os.path.join(OUTPUT_DIR, "multi_page_result.html"), "w", encoding="utf-8") as f:
                f.write(html_content)
            print("HTML output saved.")
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def test_results_endpoint(result_id):
    """Test the results endpoint"""
    print(f"\n=== Testing Results Endpoint with ID: {result_id} ===")
    
    response = requests.get(f"{RESULTS_ENDPOINT}/{result_id}")
    
    if response.status_code == 200:
        print("Success! Results endpoint working.")
        return True
    elif response.status_code == 501:
        print("Note: Results storage not implemented (status 501).")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

def run_all_tests():
    """Run all API tests"""
    print("Starting GOT-OCR 2.0 API Tests...")
    
    # Track test results
    results = {}
    result_id = None
    
    # Test 1: Plain Text OCR
    results["Plain Text OCR"] = test_plain_text_ocr()
    
    # Test 2: Format Text OCR
    results["Format Text OCR"] = test_format_text_ocr()
    
    # Test 3: Fine-grained OCR (Box)
    results["Fine-grained OCR (Box)"] = test_box_ocr()
    
    # Test 4: Fine-grained OCR (Color)
    results["Fine-grained OCR (Color)"] = test_color_ocr()
    
    # Test 5: Multi-crop OCR
    results["Multi-crop OCR"] = test_multi_crop_ocr()
    
    # Test 6: Multi-page OCR
    results["Multi-page OCR"] = test_multi_page_ocr()
    
    # Test 7: Results Endpoint (using the last result_id)
    if result_id:
        results["Results Endpoint"] = test_results_endpoint(result_id)
    
    # Print summary
    print("\n=== Test Summary ===")
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
    
    # Calculate overall success rate
    success_rate = sum(1 for result in results.values() if result) / len(results) * 100
    print(f"\nOverall Success Rate: {success_rate:.1f}%")
    
    print(f"\nTest results saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    run_all_tests()