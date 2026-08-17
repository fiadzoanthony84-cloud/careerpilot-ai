import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from backend.cv_analyzer import extract_text

pdf_path = "uploads/CV-Justice.pdf"

print(f"Testing file: {pdf_path}")

text = extract_text(pdf_path)

print("\nFIRST 1000 CHARACTERS:\n")
print(text[:1000])