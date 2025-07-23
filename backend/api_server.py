from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/app/input'
OUTPUT_FOLDER = '/app/output'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

def extract_outline(pdf_path):
    headings = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            for line in text.split('\n'):
                if line.strip().lower().startswith(('1 ', '2 ', 'i.', 'a)', '•')):
                    headings.append({
                        "text": line.strip(),
                        "page": i,
                        "level": "H2" if len(line) < 60 else "H3"
                    })
    return {
        "title": os.path.basename(pdf_path),
        "total_pages": len(pdf.pages),
        "outline": headings
    }

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    result = extract_outline(path)
    output_path = os.path.join(OUTPUT_FOLDER, filename.replace('.pdf', '.json'))
    with open(output_path, 'w') as f:
        json.dump(result, f)

    return jsonify(result)

@app.route('/api/upload-multiple', methods=['POST'])
def upload_multiple():
    files = request.files.getlist('files[]')
    persona = request.form.get('persona')
    job = request.form.get('job_to_be_done')

    if len(files) < 3 or not persona or not job:
        return jsonify({"error": "Need at least 3 PDFs and persona/job."}), 400

    results = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            result = extract_outline(path)
            result['filename'] = filename
            results.append(result)
            with open(os.path.join(OUTPUT_FOLDER, filename.replace('.pdf', '.json')), 'w') as f:
                json.dump(result, f)

    sections = [s for r in results for s in r['outline']]
    model = SentenceTransformer('all-MiniLM-L6-v2')
    job_vec = model.encode([job])[0]

    for section in sections:
        section_vec = model.encode([section['text']])[0]
        section['importance_rank'] = float(cosine_similarity([job_vec], [section_vec])[0][0])

    result_data = {
        "metadata": {
            "persona": persona,
            "job_to_be_done": job,
            "documents": [r['filename'] for r in results]
        },
        "extracted_sections": sorted(sections, key=lambda s: -s['importance_rank'])[:10],
        "sub_section_analysis": sections[:10]
    }

    return jsonify({
        "documents_processed": len(results),
        "persona_analysis": result_data,
        "individual_documents": results
    })

@app.route('/api/outlines', methods=['GET'])
def all_outlines():
    outlines = []
    for f in os.listdir(OUTPUT_FOLDER):
        if f.endswith('.json'):
            with open(os.path.join(OUTPUT_FOLDER, f)) as j:
                data = json.load(j)
                data['json_filename'] = f
                outlines.append(data)
    return jsonify(outlines)

@app.route('/api/outline/<filename>', methods=['GET'])
def one_outline(filename):
    path = os.path.join(OUTPUT_FOLDER, filename.replace('.pdf', '.json'))
    if not os.path.exists(path):
        return jsonify({"error": "Not found"}), 404
    with open(path) as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
