class PDFIntelligenceApp {
  constructor() {
    this.currentMode = null;
    this.currentPDF = null;
    this.currentOutline = null;
    this.currentPersonaAnalysis = null;
    this.adobeDCView = null;
    this.uploadedFiles = []; // Files selected by user (File objects)
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadDocumentLibrary();
    this.initializeAdobeAPI();
  }

  setupEventListeners() {
    // Single document mode
    const uploadArea = document.getElementById("uploadArea");
    const fileInput = document.getElementById("fileInput");

    if (uploadArea && fileInput) {
      uploadArea.addEventListener("click", () => fileInput.click());
      fileInput.addEventListener("change", (e) =>
        this.handleFileSelect(e.target.files[0])
      );
      uploadArea.addEventListener("dragover", this.handleDragOver.bind(this));
      uploadArea.addEventListener("dragleave", this.handleDragLeave.bind(this));
      uploadArea.addEventListener("drop", this.handleDrop.bind(this));
    }

    // Multi-document mode
    const multiFileInput = document.getElementById("multiFileInput");
    if (multiFileInput) {
      multiFileInput.addEventListener("change", (e) =>
        this.handleMultiFileSelect(e.target.files)
      );
    }

    // Analyze Documents button - now sends JSON payload as per hackathon spec
    const analyzeBtn = document.getElementById("analyzeBtn");
    if (analyzeBtn) {
      analyzeBtn.addEventListener("click", this.analyzePersona.bind(this));
    }

    // Download single document
    const downloadBtn = document.getElementById("downloadBtn");
    if (downloadBtn) {
      downloadBtn.addEventListener("click", this.downloadCurrentPDF.bind(this));
    }

    // Library actions
    const libraryPersonaBtn = document.getElementById("libraryPersonaBtn");
    const refreshLibraryBtn = document.getElementById("refreshLibraryBtn");
    if (libraryPersonaBtn) {
      libraryPersonaBtn.addEventListener(
        "click",
        this.analyzeLibraryForPersona.bind(this)
      );
    }
    if (refreshLibraryBtn) {
      refreshLibraryBtn.addEventListener(
        "click",
        this.loadDocumentLibrary.bind(this)
      );
    }
  }

  async initializeAdobeAPI() {
    if (typeof window.AdobeDC !== "undefined") {
      this.adobeDCView = new AdobeDC.View({
        clientId: "YOUR_CLIENT_ID", // Replace with actual Adobe client ID
        divId: "adobeDCView",
      });
    } else {
      console.warn("Adobe DC View SDK not loaded");
    }
  }

  setMode(mode) {
    this.currentMode = mode;
    document.getElementById("modeSelection").style.display = "none";

    if (mode === "single") {
      document.getElementById("singleDocMode").style.display = "block";
    } else if (mode === "persona") {
      document.getElementById("personaMode").style.display = "block";
    }
  }

  backToModeSelection() {
    this.currentMode = null;
    document.getElementById("modeSelection").style.display = "block";
    document.getElementById("singleDocMode").style.display = "none";
    document.getElementById("personaMode").style.display = "none";
    document.getElementById("resultsGrid").style.display = "none";
    document.getElementById("personaResults").style.display = "none";
    document.getElementById("personaContextPanel").style.display = "none";
  }

  // Single document handlers ...

  handleMultiFileSelect(files) {
    // Accumulate multiple files avoiding duplicates
    for (const file of Array.from(files)) {
      if (
        !this.uploadedFiles.some(
          (f) => f.name === file.name && f.size === file.size
        )
      ) {
        this.uploadedFiles.push(file);
      }
    }
    this.displayFileList();

    // Reset input so the same files can be re-selected if needed
    document.getElementById("multiFileInput").value = "";
  }

  displayFileList() {
    const fileList = document.getElementById("fileList");
    if (this.uploadedFiles.length === 0) {
      fileList.innerHTML = '<p style="color: #666;">No files selected</p>';
      return;
    }

    const fileListHTML = this.uploadedFiles
      .map(
        (file, index) => `
            <div class="file-item">
                <span>📄 ${file.name}</span>
                <button onclick="app.removeFile(${index})" style="background: none; border: none; color: #d32f2f; cursor: pointer;">✕</button>
            </div>
        `
      )
      .join("");

    fileList.innerHTML = fileListHTML;
  }

  removeFile(index) {
    this.uploadedFiles.splice(index, 1);
    this.displayFileList();
  }

  async analyzePersona() {
    const persona = document.getElementById("personaInput").value.trim();
    const jobToBeDone = document.getElementById("jobInput").value.trim();

    if (!persona || !jobToBeDone) {
      this.showError("Please fill in both persona and job to be done fields.");
      return;
    }

    if (this.uploadedFiles.length < 3) {
      this.showError(
        "Please upload at least 3 PDF files for persona analysis."
      );
      return;
    }
    if (this.uploadedFiles.length > 10) {
      this.showError("Please upload no more than 10 PDF files.");
      return;
    }

    this.showPersonaProgress(true);

    try {
      // Step 1: Upload files to backend (keep this step if backend requires actual files before JSON analyze)
      const formData = new FormData();
      this.uploadedFiles.forEach((file) => formData.append("files[]", file));
      formData.append("persona", persona);
      formData.append("job_to_be_done", jobToBeDone);

      const uploadResponse = await fetch("/api/upload-multiple", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("File upload failed");
      }

      // Step 2: Call analyze-persona endpoint with JSON metadata input per hackathon spec
      const payload = {
        challenge_info: {
          challenge_id: "round_1b_XXX",
          test_case_name: "specific_test_case",
        },
        documents: this.uploadedFiles.map((file) => ({
          filename: file.name,
          title: file.name,
        })),
        persona: {
          role: persona,
        },
        job_to_be_done: {
          task: jobToBeDone,
        },
      };

      const analyzeResponse = await fetch("/api/analyze-persona", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!analyzeResponse.ok) {
        throw new Error("Analysis failed");
      }

      const result = await analyzeResponse.json();
      this.currentPersonaAnalysis = result;

      await this.displayPersonaResults({ persona_analysis: result });

      this.showSuccess(
        `Successfully analyzed ${result.metadata.input_documents.length} documents for persona!`
      );
    } catch (error) {
      this.showError("Error analyzing documents: " + error.message);
    } finally {
      this.showPersonaProgress(false);
    }
  }

  // ... (keep your existing functions displayPersonaResults(), showError(), showSuccess(), showPersonaProgress(), etc.)

  // Existing helper functions not shown here remain the same

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize the app singleton instance
const app = new PDFIntelligenceApp();
