document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('quotationForm');
  const fileInput = document.getElementById('fileInput');
  const fileUploadArea = document.getElementById('fileUploadArea');
  const loadingSection = document.getElementById('loadingSection');
  const resultsSection = document.getElementById('resultsSection');
  const resultsShell = document.getElementById('resultsShell');
  const generateBtn = document.getElementById('generateBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const themeToggle = document.getElementById('themeToggle');
  const yearNow = document.getElementById('yearNow');

  // Debug: Check if elements are found
  if (!form) console.warn('Form not found!');
  if (!generateBtn) console.warn('Generate button not found!');
  if (!fileInput) console.warn('File input not found!');

  if (yearNow) yearNow.textContent = new Date().getFullYear();

  // Theme toggle (persist)
  const savedTheme = localStorage.getItem('theme') || 'light';
  setTheme(savedTheme);
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.classList.contains('theme-dark') ? 'light' : 'dark';
    setTheme(next);
  });
  function setTheme(mode) {
    if (mode === 'dark') {
      document.documentElement.classList.add('theme-dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('theme-dark');
      localStorage.setItem('theme', 'light');
    }
  }

  // Upload interactions
  fileUploadArea?.addEventListener('click', () => fileInput?.click());
  fileUploadArea?.addEventListener('dragover', (e) => { e.preventDefault(); fileUploadArea.classList.add('dragover'); });
  fileUploadArea?.addEventListener('dragleave', () => fileUploadArea.classList.remove('dragover'));
  fileUploadArea?.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files?.length > 0) {
      fileInput.files = files;
      updateFileDisplay(files[0]);
    }
  });
  fileInput?.addEventListener('change', (e) => {
    if (e.target.files?.length > 0) updateFileDisplay(e.target.files[0]);
  });

  function updateFileDisplay(file) {
    const info = document.getElementById('fileInfo');
    if (!info) return;
    info.innerHTML = `
      <div class="upload-icon text-success"><i class="fas fa-check-circle"></i></div>
      <h6 class="text-success mb-1">File Selected</h6>
      <p class="text-muted mb-0">${file.name}</p>
      <small class="text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</small>
    `;
  }

  // Also handle button click directly as fallback
  generateBtn?.addEventListener('click', function(e) {
    if (form) {
      // Trigger form validation and submission
      if (form.checkValidity()) {
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      } else {
        form.reportValidity();
      }
    }
  });

  // Form submission
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    console.log('Form submitted'); // Debug
    
    // Validate file
    if (!fileInput?.files || fileInput.files.length === 0) {
      showAlert('Please select a DXF file before submitting.', 'warning');
      return;
    }
    
    // Validate material
    const material = document.getElementById('material')?.value;
    if (!material) {
      showAlert('Please select a material.', 'warning');
      return;
    }
    
    // Validate thickness
    const thickness = document.getElementById('thickness')?.value;
    if (!thickness || parseFloat(thickness) <= 0) {
      showAlert('Please enter a valid thickness.', 'warning');
      return;
    }
    
    const formData = new FormData(form);
    
    // Show loading
    if (loadingSection) {
      loadingSection.classList.remove('d-none');
      loadingSection.style.display = 'block';
    }
    resultsSection?.classList.add('d-none');
    resultsShell?.classList.remove('d-none');
    
    // Disable button
    if (generateBtn) {
      generateBtn.disabled = true;
      generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    }
    
    try {
      console.log('Sending request to /upload'); // Debug
      const response = await fetch('/upload', { 
        method: 'POST', 
        body: formData 
      });
      
      console.log('Response status:', response.status); // Debug
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Response data:', data); // Debug
      
      if (data.success && data.id) {
        window.location.href = `/features/${encodeURIComponent(data.id)}`;
      } else {
        showAlert(data.error || 'An error occurred while processing your file.', 'danger');
        if (generateBtn) {
          generateBtn.disabled = false;
          generateBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Generate Quotation';
        }
      }
    } catch (err) {
      console.error('Error:', err); // Debug
      showAlert('Network error. Please check your connection and try again. Error: ' + err.message, 'danger');
      if (generateBtn) {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-calculator me-2"></i>Generate Quotation';
      }
    } finally {
      if (loadingSection) {
        loadingSection.style.display = 'none';
        loadingSection.classList.add('d-none');
      }
    }
  });

  function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    const container = document.querySelector('.hero-section .card-body') || document.body;
    container.prepend(alertDiv);
    setTimeout(() => alertDiv.remove(), 5000);
  }

  function renderGeometryDetails(geometry) {
    if (!geometry) return;
    // Create a verbose feature list to look "rich"
    const section = document.getElementById('resultsSection');
    if (!section) return;
    let details = document.getElementById('geometryDetails');
    if (!details) {
      details = document.createElement('div');
      details.id = 'geometryDetails';
      details.className = 'mt-4';
      section.appendChild(details);
    }
    const layers = geometry.layer_stats || {};
    const counts = [
      ['Lines', geometry.line_count],
      ['Arcs', geometry.arc_count],
      ['Circles', geometry.circle_count],
      ['Polylines', geometry.polyline_count],
      ['Splines', geometry.spline_count],
      ['Ellipses', geometry.ellipse_count],
      ['Texts', geometry.text_count],
      ['Block Refs', geometry.block_ref_count]
    ];
    const countsHtml = counts.map(([label, val]) => `<div class="col-6 col-md-3"><div class="result-card text-center"><div class="small text-muted">${label}</div><div class="result-value">${val || 0}</div></div></div>`).join('');
    const layerRows = Object.entries(layers).map(([name, cnt]) => `<tr><td>${name}</td><td class="text-end">${cnt}</td></tr>`).join('');
    const sampleEntities = (geometry.entities || []).slice(0, 50).map((e, i) => `<tr><td>${i+1}</td><td>${e.type}</td><td>${(e.length||0).toFixed ? (e.length||0).toFixed(2) : ''}</td></tr>`).join('');
    details.innerHTML = `
      <div class="d-flex align-items-center mb-3"><i class="fas fa-list text-primary me-2"></i><h5 class="mb-0">Extracted Features</h5></div>
      <div class="row g-3">${countsHtml}</div>
      <div class="row g-3 mt-3">
        <div class="col-md-6">
          <div class="card card-elevated">
            <div class="card-body">
              <h6 class="mb-3">Layer Distribution</h6>
              <table class="table table-sm mb-0"><tbody>${layerRows || '<tr><td colspan="2" class="text-muted">No layers found</td></tr>'}</tbody></table>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card card-elevated">
            <div class="card-body">
              <h6 class="mb-3">Entity Samples (max 50)</h6>
              <table class="table table-sm mb-0"><thead><tr><th>#</th><th>Type</th><th>Length (mm)</th></tr></thead><tbody>${sampleEntities || '<tr><td colspan="3" class="text-muted">No entities found</td></tr>'}</tbody></table>
            </div>
          </div>
        </div>
      </div>
    `;
  }
});


