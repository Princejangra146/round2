```markdown
# 🧠 Smart PDF Analyzer – Connecting the Dots 🔗

## 🏆 Adobe National Hackathon Submission: Challenge 1A – "Understand Your Document"

This project presents a robust and intelligent rule-based solution designed to precisely analyze PDF documents, automatically identify their core title, and generate a hierarchical structural outline (H1, H2, H3). Developed specifically for the Adobe National Hackathon, this analyzer excels at transforming unstructured PDF content into actionable, semantically rich data without relying on machine learning models, ensuring offline capability and a lightweight footprint.

## ✨ Features

* **Intelligent Text Extraction:** Leverages `pdfplumber` to accurately extract text blocks while preserving critical formatting information like font size, bold attributes, and precise spacing, crucial for structural analysis.
* **Content-Aware Heading Detection:** Employs a sophisticated rule-based engine to differentiate true structural headings from regular text. This includes analysis of font properties, positional context, word count, and a comprehensive set of semantic filters to eliminate non-heading patterns.
* **Adaptive Title Generation:** Dynamically identifies the document's primary title by analyzing font prominence and layout on the first page, with specialized logic for different document types.
* **Hierarchical Outline Generation:** Constructs a meaningful H1, H2, and H3 outline by grouping headings based on relative font sizes and page order, providing a clear navigational structure.
* **Dynamic Document Type Classification:** Employs an initial content analysis to classify documents (e.g., forms, technical documents, business proposals, educational materials) and adapts its outline extraction logic accordingly, ensuring higher accuracy.
* **Optimized Docker Deployment:** Provided as a highly optimized, multi-stage Docker image (<200MB) built on Alpine Linux. It is designed for offline execution and efficient CPU-only processing, meeting hackathon performance requirements.

## ⚙️ How It Works (Technical Overview)

The `SmartPDFAnalyzer` operates through a series of intelligent steps:
1.  **Text Block Extraction:** Each PDF page is processed to extract individual text blocks, capturing their text, font size, bold status, and coordinates.
2.  **Document Structure Analysis:** An initial pass determines the likely document type (e.g., 'form', 'technical', 'business_proposal') and establishes baseline font statistics, such as the most common body text size.
3.  **Structural Heading Identification:** Each text block is then evaluated against a weighted scoring system to determine if it's a structural heading. This system considers:
    * **Formatting:** Font size relative to body text, boldness.
    * **Position:** Horizontal alignment on the page.
    * **Content Patterns:** Regular expressions detect numbering (e.g., "1. Introduction"), capitalization, and the presence of structural keywords (e.g., "Overview," "Conclusion").
    * **Exclusion Rules:** Filters out common non-heading text like page numbers, URLs, and sentences that might superficially look like headings.
4.  **Outline Construction:** Identified headings are then grouped by font size prominence to assign hierarchical levels (H1, H2, H3). The hierarchy is further refined by page and vertical position.
5.  **Title Detection:** The document's main title is determined based on the largest font size on the first page or through specific pattern matching for known document types.

## 📂 Project Structure

```

.
├── Dockerfile                  \# Multi-stage Dockerfile for optimized image
├── main.py                     \# The core Smart PDF Analyzer logic
├── requirements.txt            \# Python dependencies (pdfplumber==0.11.4)
├── .gitignore                  \# Specifies intentionally untracked files
├── .dockerignore               \# Defines files/directories to ignore in Docker image context
├── input/                      \# Directory to place input PDF files
└── output/                     \# Directory where JSON results will be saved

````

## 🧪 Tech Stack

* **Language**: Python 3.11
* **Core Library**: [`pdfplumber==0.11.4`](https://pypi.org/project/pdfplumber/) - For robust PDF text and layout extraction.
* **Containerization**: Docker - For consistent and isolated execution environment.
    * Utilizes a multi-stage build with an Alpine Linux base for a remarkably lightweight image.

## 🚀 How to Use

Follow these steps to build and run the Smart PDF Analyzer:

### 1. Build the Docker Image

Navigate to the root directory of the project in your terminal and execute the following command:

```bash
docker build --platform linux/amd64 -t smart-pdf-analyzer .
````

### 2\. Prepare Input PDFs

Place your `.pdf` files that you wish to analyze into the `input/` directory within the project's root.

### 3\. Run the Container

Execute the Docker container. The analyzer will process all PDFs in the `input/` directory and save the resulting JSON files to the `output/` directory.

**For Linux / macOS / Git Bash:**

```bash
docker run --rm \
-v "$(pwd)/input:/app/input" \
-v "$(pwd)/output:/app/output" \
--network none \
smart-pdf-analyzer
```

**For Windows PowerShell:**

```powershell
docker run --rm -v "$PWD/input:/app/input" `
-v "$PWD/output:/app/output" --network none `
smart-pdf-analyzer
```

The `--rm` flag automatically removes the container after execution. The `-v` flags mount your local `input/` and `output/` directories to the container's `/app/input` and `/app/output` paths, respectively. `--network none` ensures the application runs completely offline, adhering to hackathon constraints.

### 4\. View Output

After the container finishes execution, you will find a `.json` file for each processed PDF in your local `output/` directory.

### 📄 Output Format

Each output JSON file will contain the detected document title and its hierarchical outline:

```json
{
    "title": "Detected Smart Title",
    "outline": [
        { "level": "H1", "text": "Introduction", "page": 1 },
        { "level": "H2", "text": "Timeline", "page": 2 },
        { "level": "H3", "text": "Project Milestones", "page": 2 }
    ]
}
```

## ✅ Hackathon Constraints Satisfied

| Constraint                           | Status           | Details                                     |
| :----------------------------------- | :--------------- | :------------------------------------------ |
| Rule-based only (no ML)              | ✅ Met           | Fully rule-based logic.                     |
| Runs offline (no internet access)    | ✅ Met           | Achieved via `--network none`.              |
| CPU-only, AMD64 compatible           | ✅ Met           | Python processing, Docker platform specified. |
| Lightweight Docker image (\<200MB)    | ✅ Met (\~140MB)  | Optimized Alpine base & multi-stage build. |
| Fast runtime (\<10s per PDF)          | ✅ Met           | Efficient `pdfplumber` and rule processing. |

## 👥 Contributors

  * **Aditya Kotnala**
  * **Anmol Pandey**
  * **Prince Jangra**

## 📜 License

This project is intended for educational and hackathon use only.

```
```