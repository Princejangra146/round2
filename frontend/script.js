class PDFIntelligenceApp {
    constructor() {
      this.currentMode = null;
      this.currentPDF = null;
      this.currentOutline = null;
      this.currentPersonaAnalysis = null;
      this.adobeDCView = null;
      this.uploadedFiles = [];
      this.init();
    }
  
    init() {
      this.setupEventListeners();
      this.loadDocumentLibrary();
      this.initializeAdobeAPI();
    }
  
    setupEventListeners() {
      // Single document mode
      const uploadArea = document.getElementById('uploadArea');
      const fileInput = document.getElementById('fileInput');
  
      if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e.target.files[0]));
        uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadArea.addEventListener('drop', this.handleDrop.bind(this));
      }
  
      // Multi-document mode
      const multiFileInput = document.getElementById('multiFileInput');
      if (multiFileInput) {
        multiFileInput.addEventListener('change', (e) => this.handleMultiFileSelect(e.target.files));
      }
  
      // 🤖 ADD THIS: Analyze button connection
      const analyzeBtn = document.getElementById('analyzeBtn');
      if (analyzeBtn) {
        analyzeBtn.addEventListener('click', this.analyzePersona.bind(this));
      }
  
      // Download single document
      const downloadBtn = document.getElementById('downloadBtn');
      if (downloadBtn) {
        downloadBtn.addEventListener('click', this.downloadCurrentPDF.bind(this));
      }
  
      // Library actions
      const libraryPersonaBtn = document.getElementById('libraryPersonaBtn');
      const refreshLibraryBtn = document.getElementById('refreshLibraryBtn');
      if (libraryPersonaBtn) {
        libraryPersonaBtn.addEventListener('click', this.analyzeLibraryForPersona.bind(this));
      }
      if (refreshLibraryBtn) {
        refreshLibraryBtn.addEventListener('click', this.loadDocumentLibrary.bind(this));
      }
    }
  
    // keep all your other methods the same
    // ...
  
    escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
  }
  
  // 🟢 INIT THE APP
  const app = new PDFIntelligenceApp();
  