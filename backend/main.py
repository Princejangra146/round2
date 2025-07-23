#!/usr/bin/env python3

import os
import sys
from pdf_processor import PDFProcessor

def main():
    """Main entry point for Docker container"""
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    print("Starting PDF Outline Extraction...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    processor = PDFProcessor()
    processor.process_pdfs(input_dir, output_dir)
    
    print("Processing complete!")

if __name__ == "__main__":
    main()
