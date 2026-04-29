import os
from markitdown import MarkItDown

md = MarkItDown()

files = [
    r"c:\Users\01102088\Desktop\sgIFC\Annex - Summary of Changes - 2023-09.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\Annex - Summary of Changes - 2024-11.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\Annex - Summary of Changes COP Edition 3.1.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\C2D_IFC-SG Demonstration Meeting.pptx",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X Code of Practice.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X COP 2.1 Edition 2024-11.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X COP 3 Edition 2025-09.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X COP 3.1 Edition 2025-12.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X COP First Edition 2023-09.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\CORENET X COP Second Edition 2024-11.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\IFC-SG Onboarding Checklist.pdf",
    r"c:\Users\01102088\Desktop\sgIFC\step-1-ifc-sg-101-(sandbox).pdf"
]

for file_path in files:
    try:
        print(f"Processing: {file_path}")
        result = md.convert(file_path)
        out_path = os.path.splitext(file_path)[0] + ".md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        print(f"Successfully converted to {out_path}")
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
