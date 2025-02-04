title = """# GOT-OCR 2.0: Transformers 🤗 implementation demo"""

description = """
This demo utilizes the **Transformers implementation of GOT-OCR 2.0** to extract text from images.
The GOT-OCR 2.0 model was introduced in the paper:
[**General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model**](https://arxiv.org/abs/2409.01704)
by *Haoran Wei, Chenglong Liu, Jinyue Chen, Jia Wang, Lingyu Kong, Yanming Xu, Zheng Ge, Liang Zhao, Jianjian Sun, Yuang Peng, Chunrui Han, and Xiangyu Zhang*.
### Key Features
GOT-OCR 2.0 is a **state-of-the-art OCR model** designed to handle a wide variety of tasks, including:
- **Plain Text OCR**
- **Formatted Text OCR**
- **Fine-grained OCR**
- **Multi-crop OCR**
- **Multi-page OCR**
### Beyond Text
GOT-OCR 2.0 has also been fine-tuned to work with non-textual data, such as:
- **Charts and Tables**
- **Math and Molecular Formulas**
- **Geometric Shapes**
- **Sheet Music**
Explore the capabilities of this cutting-edge model through this interactive demo!
"""

tasks = [
    "Plain Text OCR",
    "Format Text OCR",
    "Fine-grained OCR (Box)",
    "Fine-grained OCR (Color)",
    "Multi-crop OCR",
    "Multi-page OCR",
]

ocr_types = ["ocr", "format"]
ocr_colors = ["red", "green", "blue"]
stop_str = "<|im_end|>"