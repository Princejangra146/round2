from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from pdf_processor import PDFProcessor   # Your existing class
from utils.persona_analyzer import PersonaAnalyzer  # Your existing class

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/app/input'
OUTPUT_FOLDER = '/app/output'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/analyze-persona', methods=['POST'])
def analyze_persona():
    data = request.get_json()

    challenge_info = data.get("challenge_info", {})
    documents = data.get("documents", [])
    persona_obj = data.get("persona", {})
    job_obj = data.get("job_to_be_done", {})

    persona_role = persona_obj.get("role", "")
    job_task = job_obj.get("task", "")

    input_filenames = [doc.get("filename") for doc in documents if "filename" in doc]

    # Load and process each document
    processor = PDFProcessor()
    results = []

    for doc in documents:
        filename = doc.get("filename")
        title = doc.get("title", "Untitled")
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Sanity check: file should exist
        if not os.path.exists(file_path):
            continue  # or handle error

        # Extract outline/sections here using your PDFProcessor or similar
        outline_result = processor.extractor.extract_outline(file_path)
        outline_result['filename'] = filename
        outline_result['title'] = title
        results.append(outline_result)

        # Save or cache JSON result if needed
        output_path = os.path.join(OUTPUT_FOLDER, filename.replace('.pdf', '.json'))
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outline_result, f, indent=2, ensure_ascii=False)

    # Flatten all extracted sections from all documents
    all_sections = []
    for res in results:
        # `outline` is assumed list of dict with 'text', 'page', etc.
        for section in res.get('outline', []):
            all_sections.append({
                "document": res['filename'],
                "section_title": section.get('text', ''),
                "page_number": section.get('page', None),
            })

    # Perform persona-driven importance ranking (using your PersonaAnalyzer)
    analyzer = PersonaAnalyzer()
    # Assuming your analyzer can consume these parameters and return ranking and refined contents.
    analysis_result = analyzer.analyze_documents_for_persona(
        results, persona_role, job_task
    )

    # The analysis_result should include ranked sections and subsection analysis
    # Here, adapt to produce output keys expected, e.g.:
    # extracted_sections and subsection_analysis

    # Example formatting:
    extracted_sections = []
    subsection_analysis = []

    # Fill extracted_sections and subsection_analysis from analyzer output accordingly.
    # For demo, using placeholders:
    for section in analysis_result.get('extracted_sections', []):
        extracted_sections.append({
            "document": section.get('document', ''),
            "section_title": section.get('section_title', ''),
            "importance_rank": section.get('importance_rank', 1),
            "page_number": section.get('page_number', 0),
        })

    for subsec in analysis_result.get('sub_section_analysis', []):
        subsection_analysis.append({
            "document": subsec.get('document', ''),
            "refined_text": subsec.get('refined_text', ''),
            "page_number": subsec.get('page_number', 0),
        })

    response = {
        "metadata": {
            "input_documents": input_filenames,
            "persona": persona_role,
            "job_to_be_done": job_task
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
