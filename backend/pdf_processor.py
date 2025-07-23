import os
import json
from utils.outline_extractor import OutlineExtractor

class PDFProcessor:
    def __init__(self):
        self.extractor = OutlineExtractor()
        
    def process_pdfs(self, input_dir: str, output_dir: str):
        """Process all PDFs in input directory"""
        if not os.path.exists(input_dir):
            print(f"Input directory {input_dir} does not exist")
            return
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            output_file = os.path.splitext(pdf_file)[0] + '.json'
            output_path = os.path.join(output_dir, output_file)
            
            print(f"Processing {pdf_file}...")
            
            result = self.extractor.extract_outline(pdf_path)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Saved outline to {output_file}")

if __name__ == "__main__":
    processor = PDFProcessor()
    processor.process_pdfs("/app/input", "/app/output")
