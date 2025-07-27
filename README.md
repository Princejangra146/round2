# Adobe PDF Intelligence - Connecting the Dots

## 🧠 Rethink Reading. Rediscover Knowledge. Connect the Dots.

This project, "Adobe PDF Intelligence - Connecting the Dots," is a modern web application designed to revolutionize how users interact with PDF documents. Leveraging intelligent outline extraction and persona-driven analysis, it offers a sophisticated platform for an enhanced PDF reading and research experience. The application integrates seamlessly with the Adobe PDF Embed API for a professional viewing experience.

## ✨ Features

  * **Intelligent PDF Processing**: The backend extracts structured outlines from PDFs using advanced text analysis techniques, identifying headings and their hierarchical levels (H1, H2, H3) based on font size and common patterns. It can also extract the document title from the first page.
  * **Persona-Driven Analysis**: Users can define a persona and a "job to be done" to analyze multiple documents. The application ranks sections within documents based on their relevance to the defined persona and job requirements using semantic similarity (or a keyword-based fallback if semantic tools are unavailable). It also provides refined summaries of key subsections aligned with the user's context.
  * **Interactive Web Interface**: The frontend provides a beautiful and responsive design with intuitive drag-and-drop functionality for single PDF uploads. It also supports multi-file selection for persona analysis.
  * **Adobe PDF Embed Integration**: For a professional and interactive PDF viewing experience, the application utilizes the Adobe PDF Embed API, allowing users to view processed documents directly within the interface.
  * **Smart Insights**: Beyond just outlines, the application aims to provide AI-powered document analysis and recommendations, enriching the user's understanding of the content.
  * **Document Library**: A dedicated section to manage and revisit processed documents, offering a quick overview and the ability to trigger further persona analysis on selected files.
  * **Real-time Processing**: Features progress indicators for both file uploads and persona analysis, ensuring a responsive user experience.

## 🚀 Quick Start

To get the application up and running quickly, follow these steps:

### Prerequisites

  * Docker and Docker Compose installed on your system.
  * An Adobe PDF Embed API Client ID (replace `"YOUR_CLIENT_ID"` in `script.js` with your actual client ID).

### Build and Run

1.  **Clone the repository** (if you haven't already):

    ```bash
    git clone <repository-url>
    cd round2-main
    ```

2.  **Place your PDF files**: Create an `input` folder in the root directory if it doesn't exist (it should be automatically created by the `Dockerfile`). Place any PDF files you wish to process in this `input` directory.

3.  **Build and run the Docker containers**:

    ```bash
    docker-compose up --build
    ```

    This command will:

      * Build the `webapp` service using the `Dockerfile`.
      * Install necessary Python dependencies (Flask, pdfplumber, transformers, torch, etc.).
      * Set up Nginx to serve the frontend.
      * Map port `80` of the container to port `80` on your host.
      * Mount the `./input` and `./output` directories from your host into the container, allowing persistent storage of input PDFs and generated JSON outlines.
      * Execute the `start.sh` script (which starts `gunicorn` for the Flask API and Nginx).

4.  **Access the application**: Once the containers are running, open your web browser and navigate to `http://localhost`.

### Project Structure

The project follows a modular structure to ensure maintainability and scalability:

```
round2-main/
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── README.md (this file)
├── backend/
│   ├── api_server.py
│   ├── main.py
│   ├── pdf_processor.py
│   └── requirements.txt
│   └── utils/
│       ├── outline_extractor.py
│       ├── persona_analyzer.py
│       └── __init__.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
└── start.sh
└── nginx.conf
```

  * **`.dockerignore`**: Specifies files and directories to be ignored by Docker when building the image, optimizing build context.
  * **`docker-compose.yml`**: Defines the services (currently `webapp`), networks, volumes, and environment variables for the Dockerized application.
  * **`Dockerfile`**: Contains instructions for building the Docker image, setting up the Python environment, installing dependencies, and configuring Nginx.
  * **`backend/`**: Contains all server-side logic.
      * **`api_server.py`**: The main Flask application that exposes RESTful APIs for PDF processing and persona analysis.
      * **`main.py`**: A standalone script for batch PDF processing, primarily used for initial setup or background tasks.
      * **`pdf_processor.py`**: Encapsulates the logic for processing PDF files, utilizing the `OutlineExtractor`.
      * **`requirements.txt`**: Lists all Python dependencies required by the backend, including Flask, pdfplumber, transformers, torch, and scikit-learn.
      * **`utils/`**: Utility modules for core functionalities.
          * **`outline_extractor.py`**: Handles the extraction of structured outlines (headings, pages, font sizes) from PDF documents using `pdfplumber`.
          * **`persona_analyzer.py`**: Implements the logic for analyzing documents based on user-defined personas and job requirements, utilizing `sentence-transformers` for semantic similarity.
          * **`__init__.py`**: An empty file indicating that `utils` is a Python package.
  * **`frontend/`**: Contains all client-side code.
      * **`index.html`**: The main HTML file defining the structure of the web application.
      * **`script.js`**: Contains the JavaScript logic for handling user interactions, API calls to the backend, and integration with the Adobe PDF Embed API.
      * **`styles.css`**: Provides the styling for the web application, ensuring a modern and responsive user interface.
  * **`start.sh`**: A shell script executed by the Docker container to start both Nginx (for the frontend) and Gunicorn (for the Flask backend).
  * **`nginx.conf`**: Nginx configuration file to serve static frontend assets and proxy API requests to the Flask backend.

## 🛠️ Technologies Used

### Frontend

  * **HTML5**
  * **CSS3**
  * **JavaScript (ES6+)**
  * **Adobe PDF Embed API**

### Backend

  * **Python 3.11**
  * **Flask**
  * **Gunicorn**
  * **Flask-CORS**
  * **pdfplumber**
  * **Hugging Face Transformers**
  * **PyTorch**
  * **Sentence-Transformers**
  * **scikit-learn**
  * **NLTK**
  * **Pandas**
  * **Numpy**

### Infrastructure

  * **Docker**
  * **Docker Compose**
  * **Nginx**

## 🎯 How to Use

### Single Document Mode

1.  Navigate to `http://localhost`.
2.  Select "Single Document" mode.
3.  Drag and drop a PDF file into the designated area, or click to browse and select a file.
4.  The application will process the PDF, extract its outline, and display it alongside the PDF viewer.
5.  You can then navigate the document using the extracted outline and download the processed PDF.

### Persona Analysis Mode

1.  Navigate to `http://localhost`.
2.  Select "Persona Analysis" mode.
3.  Enter the "Persona" (e.g., "PhD Researcher in NLP") and "Job to be Done" (e.g., "Analyze 5 papers to summarize key results").
4.  Upload 3 to 10 PDF files for analysis using the multi-file input.
5.  Click "Analyze Documents".
6.  The application will process the documents and provide ranked sections and refined subsection analysis based on your defined persona and job, helping you connect the dots across multiple resources.

## 💡 Future Enhancements

  * Enhanced Outline Extraction
  * Advanced AI Insights
  * User Authentication and Storage
  * Interactive Outline Editing
  * Export Options
  * Multi-language Support

## 👥 Contributors

  * Aditya Kotnala
  * Anmol Pandey
  * Prince Jangra

## 📜 License

For educational & hackathon use only.
