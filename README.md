# CNC AI Quotation Generator

A professional, industry-grade CNC machining cost estimation platform that automatically generates quotations from CAD files. This application processes DXF files, extracts comprehensive geometry information, calculates machining costs, and generates professional PDF quotations with AI-powered optimization recommendations.

---

## 📋 Table of Contents

1. [Features Overview](#-features-overview)
2. [Installation & Setup](#-installation--setup)
3. [Quick Start Guide](#-quick-start-guide)
4. [System Architecture](#-system-architecture)
5. [Core Functionalities](#-core-functionalities)
6. [Algorithm Explanations](#-algorithm-explanations)
7. [AI Features](#-ai-features)
8. [Usage Guide](#-usage-guide)
9. [Configuration](#-configuration)
10. [Troubleshooting](#-troubleshooting)
11. [Project Structure](#-project-structure)

---

## 🚀 Features Overview

### Core Functionality
- ✅ **DXF File Processing**: Upload and parse DXF files with precision
- ✅ **Geometry Extraction**: Automatically extract lines, arcs, circles, polylines, splines, ellipses
- ✅ **Material Database**: Support for 6 common materials (steel, aluminum, plastic, wood, brass, copper)
- ✅ **Smart Cost Calculation**: AI-powered cost and time estimation
- ✅ **Professional PDF Generation**: Industry-grade quotation documents with company branding
- ✅ **Complexity Analysis**: Automatic complexity scoring and entity breakdown
- ✅ **Layer Statistics**: Detailed layer-by-layer analysis

### AI-Powered Features
- 🤖 **Material Recommendations**: AI-suggested material alternatives with cost-benefit analysis
- 🛣️ **Path Optimization**: TSP-based cutting path optimization with visualizations
- 📐 **Nesting Optimization**: Optimal part arrangement on material sheets
- 💡 **Design Suggestions**: AI-powered manufacturability improvements
- 📊 **Manufacturing Insights**: Expert recommendations for production

### Interactive Features
- 📈 **Real-time Visualization**: Canvas-based path and nesting visualizations
- 📊 **Interactive Charts**: Entity distribution and layer statistics
- 🎨 **Modern UI**: Responsive, industry-grade dashboard
- ⚡ **Async Loading**: Fast page loads with background AI processing

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Operating System**: Windows, macOS, or Linux
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)

### Step-by-Step Installation

#### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd CAD

# Or download and extract the ZIP file
# Navigate to the extracted folder
cd CAD
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed Flask-2.3.3 ezdxf-1.1.1 reportlab-4.0.4 ...
```

#### 4. Set Up Environment Variables (Optional - for AI Features)

Create a `.env` file in the project root:

```env
# For OpenAI (if using)
OPENAI_API_KEY=your-openai-key-here
OPENAI_MODEL=gpt-3.5-turbo

# For OpenRouter (Recommended - Free AI models)
USE_OPENROUTER=true
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

**Note**: You can get a free OpenRouter API key at [https://openrouter.ai/keys](https://openrouter.ai/keys)

#### 5. Verify Installation

```bash
python -c "from app import app; print('✓ Installation successful!')"
```

#### 6. Run the Application

```bash
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### 7. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🎯 Quick Start Guide

![Homepage](screenshots/screenshot-01-homepage.png)

### Basic Workflow

1. **Upload DXF File**
   - Click "Upload Your CAD File" or drag and drop
   - Select a `.dxf` file (max 16MB)
   - ![Upload Interface](screenshots/screenshot-03-upload-interface.png)

2. **Select Material & Thickness**
   - Choose material type (Steel, Aluminum, etc.)
   - Enter thickness in millimeters
   - ![File Selected](screenshots/screenshot-04-file-selected.png)

3. **Generate Quotation**
   - Click "Generate Quotation"
   - Wait for processing (usually 2-5 seconds)
   - ![Processing](screenshots/screenshot-05-processing.png)

4. **View Results**
   - Review geometry analysis
   - Check cost breakdown
   - View AI recommendations
   - ![Results Overview](screenshots/screenshot-06-results-overview.png)

5. **Download PDF**
   - Click "Generate PDF Quotation"
   - Professional quotation document downloads
   - ![PDF Quotation](screenshots/screenshot-22-pdf-page1.png)

### First-Time User Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs without errors
- [ ] Can access `http://localhost:5000`
- [ ] Test DXF file uploaded successfully
- [ ] PDF quotation generated

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (User Interface)│
└────────┬─────────┘
         │ HTTP Requests
         ▼
┌─────────────────┐
│   Flask App     │  ← app.py (Main Application)
│   (Backend)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    ▼         ▼              ▼              ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   CAD   │ │  Cost    │ │   PDF    │ │    AI    │
│Processor│ │Calculator│ │ Generator│ │  Advisor │
└─────────┘ └──────────┘ └──────────┘ └──────────┘
    │            │            │            │
    ▼            ▼            ▼            ▼
┌──────────────────────────────────────────────┐
│         Core Processing Modules              │
│  - Geometry Extraction                       │
│  - Cost Calculation                          │
│  - PDF Generation                            │
│  - AI Recommendations                        │
└──────────────────────────────────────────────┘
```

### Module Responsibilities

| Module | Responsibility | Key Functions |
|--------|---------------|---------------|
| `app.py` | Flask web server, routing, request handling | File upload, result caching, API endpoints |
| `cad_processor.py` | DXF parsing, geometry extraction | Entity parsing, length calculation, complexity scoring |
| `cost_calculator.py` | Cost and time estimation | Material cost, labor cost, machining time |
| `pdf_generator.py` | Professional PDF generation | Quotation formatting, branding, tables |
| `ai_advisor.py` | AI-powered recommendations | Material suggestions, path optimization, nesting |
| `path_optimizer.py` | TSP path optimization | Nearest neighbor algorithm, path calculation |
| `nesting_optimizer.py` | Material sheet nesting | Bin packing, utilization calculation |

---

## 🔧 Core Functionalities

### 1. DXF File Processing

![File Upload](screenshots/screenshot-03-upload-interface.png)

**What it does:**
- Parses DXF (Drawing Exchange Format) files
- Extracts all geometric entities
- Calculates dimensions and measurements

**Supported Entity Types:**
- **Lines**: Straight line segments
- **Arcs**: Curved segments with radius and angles
- **Circles**: Complete circular shapes
- **Polylines**: Connected line segments
- **Splines**: Smooth curves (approximated)
- **Ellipses**: Elliptical shapes (approximated)
- **Text**: Text entities (counted, not measured)
- **Block References**: Inserted blocks (counted)

**How it works:**
1. File is uploaded and validated
2. `ezdxf` library parses the DXF structure
3. Each entity is processed individually
4. Geometric properties are extracted
5. Measurements are calculated and stored

**Output:**
- Total cutting length
- Entity counts by type
- Bounding box dimensions
- Layer statistics
- Complexity metrics

---

### 2. Geometry Analysis

![Results Overview](screenshots/screenshot-06-results-overview.png)
![Complexity Analysis](screenshots/screenshot-07-complexity.png)
![Drawing Dimensions](screenshots/screenshot-08-dimensions.png)

**Bounding Box Calculation:**
- Finds minimum and maximum X/Y coordinates
- Calculates width, height, and area
- Determines drawing origin

**Complexity Scoring:**
- Analyzes entity count and diversity
- Considers layer count
- Evaluates curve complexity (splines, arcs)
- Calculates entity density
- Generates 0-100 complexity score

**Entity Breakdown:**
- Counts each entity type
- Calculates percentage distribution
- Measures individual entity lengths
- Tracks layer usage

---

### 3. Cost Calculation

**Components:**
1. **Material Cost**
   - Based on cutting length × thickness
   - Material-specific pricing
   - Includes kerf width (1mm)

2. **Labor Cost**
   - Machining time × hourly rate
   - Material-specific rates
   - Includes setup and tool change time

3. **Total Cost**
   - Material + Labor + Setup
   - Includes 18% GST (Indian market)
   - Safety factor applied (15%)

**Formula:**
```
Material Cost = (Cutting Length × Thickness × Material Price per cm³)
Labor Cost = (Machining Time × Hourly Rate)
Total Cost = (Material + Labor + Setup) × 1.18 (GST)
```

---

### 4. PDF Quotation Generation

![PDF Page 1](screenshots/screenshot-22-pdf-page1.png)
![PDF Page 2](screenshots/screenshot-23-pdf-page2.png)
![PDF Cost Breakdown](screenshots/screenshot-24-pdf-cost-detail.png)

**Features:**
- Professional header with company branding
- Quotation number (auto-generated)
- Executive summary boxes
- Detailed project specifications
- Technical entity breakdown
- Comprehensive cost breakdown
- Terms and conditions
- Signature section
- Page numbering and footer

**Sections:**
1. **Header**: Company info, quotation number, dates
2. **Executive Summary**: Key metrics at a glance
3. **Project Details**: Material, dimensions, complexity
4. **Technical Specs**: Entity breakdown table
5. **Cost Breakdown**: Itemized costs with GST
6. **Terms & Conditions**: Payment, lead time, warranty
7. **Signature**: Prepared by and authorized signature

---

## 🧮 Algorithm Explanations

### 1. Complexity Score Algorithm

**Purpose:** Quantify the manufacturing complexity of a CAD drawing (0-100 scale)

**Formula:**
```python
complexity_score = (
    entity_count_factor * 30 +      # 30% weight
    entity_diversity_factor * 20 + # 20% weight
    layer_complexity_factor * 15 +  # 15% weight
    curve_complexity_factor * 20 +   # 20% weight
    size_factor * 10 +               # 10% weight
    density_factor * 5               # 5% weight
)
```

**Factors:**
- **Entity Count**: More entities = higher complexity
- **Entity Diversity**: Mix of types = higher complexity
- **Layer Count**: More layers = higher complexity
- **Curve Complexity**: Splines and arcs = higher complexity
- **Drawing Size**: Larger drawings = slightly higher complexity
- **Entity Density**: Dense drawings = higher complexity

**Example:**
- Simple rectangle (4 lines): ~15/100
- Complex mechanical part (100+ entities): ~75/100
- Very complex design (curves, many layers): ~90/100

---

### 2. TSP Path Optimization Algorithm

**Purpose:** Optimize cutting path to minimize travel distance

**Algorithm: Nearest Neighbor with 2-opt Improvement**

**Step-by-Step:**

1. **Extract Points**
   - Get start/end points of all lines
   - Get center points of circles
   - Create point list with entity mapping

2. **Calculate Original Distance**
   - Sum distances in original entity order
   - This is the baseline

3. **Nearest Neighbor TSP**
   ```
   Start with first point
   While unvisited points exist:
       Find nearest unvisited point
       Add to path
       Move to that point
   ```

4. **2-opt Improvement** (Optional)
   - Try reversing path segments
   - Keep improvements that reduce distance
   - Iterate until no improvement

5. **Calculate Savings**
   ```
   Original Distance - Optimized Distance
   Savings % = (Savings / Original) × 100
   ```

**Time Complexity:** O(n²) where n = number of points

**Expected Savings:** 10-30% reduction in travel distance

**Visualization:**
- Original path shown in one color
- Optimized path shown in another color
- Distance savings displayed

---

### 3. Nesting Optimization Algorithm

**Purpose:** Maximize material utilization by optimal part arrangement

**Algorithm: Grid-Based Bin Packing**

**Step-by-Step:**

1. **Get Part Dimensions**
   - Extract bounding box (width × height)
   - Calculate part area

2. **For Each Standard Sheet Size:**
   ```
   Calculate parts per row: (Sheet Width - Spacing) / (Part Width + Spacing)
   Calculate parts per column: (Sheet Height - Spacing) / (Part Height + Spacing)
   Total parts = parts_per_row × parts_per_column
   ```

3. **Calculate Metrics:**
   ```
   Used Area = Total Parts × Part Area
   Utilization % = (Used Area / Sheet Area) × 100
   Waste % = 100 - Utilization %
   Cost per Part = Sheet Cost / Total Parts
   ```

4. **Select Best Arrangement:**
   - Highest utilization
   - Lowest waste
   - Best cost per part

5. **Generate Layout:**
   - Calculate X/Y positions for each part
   - Apply 5mm spacing between parts
   - Create visual layout coordinates

**Standard Sheet Sizes:**
- 1000 × 2000 mm
- 1250 × 2500 mm
- 1500 × 3000 mm
- 2000 × 4000 mm

**Expected Utilization:** 60-85% (depending on part size)

**Visualization:**
- Canvas-based layout
- Color-coded parts
- Grid overlay for scale
- Part numbers and dimensions

---

### 4. Cost Calculation Algorithm

**Purpose:** Accurate cost estimation for CNC machining

**Machining Time Calculation:**
```python
Cutting Time = Total Length / Feed Rate (mm/min)
Total Time = Cutting Time + Setup Time + Tool Change Time
Final Time = Total Time × Safety Factor (1.15)
```

**Material Cost Calculation:**
```python
Material Area = Cutting Length × (Thickness + Kerf Width)
Material Volume (cm³) = Material Area / 1000
Material Cost = Volume × Material Price per cm³
```

**Labor Cost Calculation:**
```python
Labor Cost = (Machining Time / 60) × Hourly Rate
```

**Total Cost:**
```python
Subtotal = Material Cost + Labor Cost + Setup Cost
GST (18%) = Subtotal × 0.18
Total = Subtotal + GST
```

**Material-Specific Parameters:**

| Material | Feed Rate (mm/min) | Material Cost (₹/cm³) | Hourly Rate (₹) |
|----------|-------------------|----------------------|-----------------|
| Steel | 300 | 6.5 | 1800 |
| Aluminum | 600 | 20.0 | 1600 |
| Plastic | 800 | 3.0 | 1200 |
| Wood | 1200 | 1.5 | 900 |
| Brass | 400 | 60.0 | 1700 |
| Copper | 350 | 75.0 | 1800 |

---

### 5. Entity Length Calculation Algorithms

**Line Length:**
```python
length = √((x₂ - x₁)² + (y₂ - y₁)²)
```

**Arc Length:**
```python
angle_diff = end_angle - start_angle (in radians)
length = radius × angle_diff
```

**Circle Length:**
```python
length = 2 × π × radius
```

**Polyline Length:**
```python
total = 0
for each segment:
    length = √((x₂ - x₁)² + (y₂ - y₁)²)
    total += length
```

**Spline Length (Approximation):**
```python
Sample 51 points along spline
Calculate distance between consecutive points
Sum all distances
```

**Ellipse Length (Ramanujan's Approximation):**
```python
a = major_axis / 2
b = minor_axis / 2
h = ((a - b)²) / ((a + b)²)
length = π × (a + b) × (1 + (3h)/(10 + √(4 - 3h)))
```

---

## 🤖 AI Features

### 1. Material Recommendations

![Material Recommendations](screenshots/screenshot-14-material-recommendations.png)

**How it works:**
- AI analyzes geometry complexity
- Considers material properties
- Suggests alternatives with cost-benefit analysis
- Provides pros/cons for each material

**Output includes:**
- Alternative materials
- Cost comparison
- Time savings/losses
- Best use cases
- Pros and cons

---

### 2. Path Optimization (AI + Algorithm)

![Path Optimization](screenshots/screenshot-15-path-optimization.png)
![TSP Results](screenshots/screenshot-16-tsp-results.png)
![Path Visualization](screenshots/screenshot-25-path-toggle.png)

**AI Analysis:**
- Identifies inefficient cutting patterns
- Suggests optimization strategies
- Estimates time savings

**TSP Algorithm:**
- Calculates optimal cutting sequence
- Minimizes travel distance
- Provides visual path comparison

**Output:**
- Original vs optimized distance
- Percentage savings
- Step-by-step path details
- Visual path graph

---

### 3. Nesting Optimization (AI + Algorithm)

![Nesting Section](screenshots/screenshot-17-nesting-section.png)
![Nesting Results](screenshots/screenshot-18-nesting-results.png)
![Nesting Table](screenshots/screenshot-19-nesting-table.png)
![Nesting Layout](screenshots/screenshot-26-nesting-zoomed.png)

**AI Analysis:**
- Suggests sheet sizes
- Recommends rotation strategies
- Identifies waste reduction opportunities

**Algorithm:**
- Calculates optimal part arrangement
- Tests multiple sheet sizes
- Generates visual layout

**Output:**
- Best sheet size
- Parts per sheet
- Material utilization %
- Waste percentage
- Visual nesting layout
- Cost per part

---

### 4. Design Optimization Suggestions

![Design Suggestions](screenshots/screenshot-20-design-suggestions.png)

**AI analyzes:**
- Geometry complexity
- Manufacturing feasibility
- Cost drivers
- Quality considerations

**Suggests:**
- Geometry simplifications
- Feature modifications
- Tolerance adjustments
- Material changes

---

### 5. Manufacturing Insights

![Manufacturing Insights](screenshots/screenshot-21-manufacturing-insights.png)

**Provides:**
- Manufacturing challenges
- Tool recommendations
- Quality tips
- Best practices
- Production considerations

---

## 📖 Usage Guide

### Basic Quotation Generation

1. **Navigate to Home Page**
   - URL: `http://localhost:5000`
   - ![Homepage](screenshots/screenshot-01-homepage.png)

2. **Upload DXF File**
   - Click upload area or drag & drop
   - Select `.dxf` file
   - ![Upload](screenshots/screenshot-03-upload-interface.png)

3. **Select Parameters**
   - Material: Choose from dropdown
   - Thickness: Enter in mm (e.g., 5.0)
   - ![File Selected](screenshots/screenshot-04-file-selected.png)

4. **Generate Quotation**
   - Click "Generate Quotation"
   - Wait for processing
   - ![Processing](screenshots/screenshot-05-processing.png)

5. **View Results**
   - Geometry analysis
   - Cost breakdown
   - Entity statistics
   - ![Results](screenshots/screenshot-06-results-overview.png)
   - ![Entity Chart](screenshots/screenshot-10-entity-chart.png)
   - ![Layer Stats](screenshots/screenshot-11-layer-stats.png)

6. **Download PDF**
   - Click "Generate PDF Quotation"
   - PDF downloads automatically
   - ![PDF](screenshots/screenshot-22-pdf-page1.png)

---

### Using AI Recommendations

![AI Loading](screenshots/screenshot-13-ai-loading.png)

1. **After Generating Quotation**
   - Click "View AI Recommendations" button
   - Or navigate to AI Recommendations page

2. **Wait for AI Analysis** (if first time)
   - Loading indicator shows progress
   - Takes 10-30 seconds

3. **Explore Recommendations**
   - Material alternatives
   - Path optimization
   - Nesting optimization
   - Design suggestions

4. **Interactive Features**
   - Click "Calculate TSP Path" for path optimization
   - Click "Calculate Optimal Nesting" for nesting
   - View visualizations

---

### Path Optimization Workflow

1. **Navigate to AI Recommendations**
2. **Scroll to Path Optimization section**
   - ![Path Section](screenshots/screenshot-15-path-optimization.png)
3. **Click "Calculate TSP Path"**
4. **View Results:**
   - Original distance
   - Optimized distance
   - Savings percentage
   - Path details table
   - ![TSP Results](screenshots/screenshot-16-tsp-results.png)
5. **Visual Comparison:**
   - Canvas shows original vs optimized
   - Toggle between views
   - ![Path Visualization](screenshots/screenshot-25-path-toggle.png)

---

### Nesting Optimization Workflow

1. **Navigate to AI Recommendations**
2. **Scroll to Nesting Optimization section**
   - ![Nesting Section](screenshots/screenshot-17-nesting-section.png)
3. **Click "Calculate Optimal Nesting"**
4. **View Results:**
   - Best sheet size
   - Parts per sheet
   - Utilization percentage
   - Waste percentage
   - Cost per part
   - ![Nesting Results](screenshots/screenshot-18-nesting-results.png)
   - ![Nesting Table](screenshots/screenshot-19-nesting-table.png)
5. **Visual Layout:**
   - Canvas shows part arrangement
   - Color-coded parts
   - Grid overlay
   - Dimensions displayed
   - ![Nesting Layout](screenshots/screenshot-26-nesting-zoomed.png)

---

## ⚙️ Configuration

### Company Information

Edit `pdf_generator.py`:

```python
self.company_name = "Your Company Name"
self.company_address = "Your Address"
self.company_city = "Your City"
self.company_phone = "+91-XXXXXXXXXX"
self.company_email = "info@yourcompany.com"
self.company_website = "www.yourcompany.com"
```

### Material Properties

Edit `cost_calculator.py`:

```python
# Material costs (₹ per cm³)
self.material_costs = {
    'steel': 0.0065,
    'aluminum': 0.0200,
    # Add/modify as needed
}

# Machine hourly rates (₹)
self.machine_rates = {
    'steel': 1800.0,
    'aluminum': 1600.0,
    # Add/modify as needed
}

# Feed rates (mm/min)
self.feed_rates = {
    'steel': 300,
    'aluminum': 600,
    # Add/modify as needed
}
```

### AI Configuration

Edit `.env` file:

```env
# Use OpenRouter (recommended for free AI)
USE_OPENROUTER=true
OPENROUTER_API_KEY=your-key-here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free

# Or use OpenAI
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### Standard Sheet Sizes

Edit `nesting_optimizer.py`:

```python
self.standard_sheets = [
    {"name": "1000x2000mm", "width": 1000, "height": 2000, ...},
    # Add custom sheet sizes
]
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. **"Module not found" Error**

**Problem:** Missing dependencies

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. **"Port 5000 already in use"**

**Problem:** Another application using port 5000

**Solution:**
- Change port in `app.py`:
  ```python
  app.run(port=5001)  # Use different port
  ```
- Or stop the other application

#### 3. **"DXF file not processing"**

**Problem:** Invalid or corrupted DXF file

**Solution:**
- Verify DXF file opens in CAD software
- Check file size (max 16MB)
- Ensure file is valid DXF format

#### 4. **"AI recommendations not loading"**

**Problem:** API key not configured or invalid

**Solution:**
- Check `.env` file exists
- Verify API key is correct
- Test API key separately
- Check internet connection

#### 5. **"PDF generation fails"**

**Problem:** ReportLab or file permission issues

**Solution:**
```bash
pip install --upgrade reportlab
# Ensure temp_pdfs directory exists and is writable
```

#### 6. **"Canvas visualization not showing"**

**Problem:** JavaScript errors or browser compatibility

**Solution:**
- Check browser console for errors
- Try different browser
- Clear browser cache
- Ensure JavaScript is enabled

---

### Debug Mode

Enable debug mode in `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True)  # Shows detailed error messages
```

---

### Logging

Check console output for:
- File processing errors
- Calculation issues
- API connection problems
- PDF generation errors

---

## 📁 Project Structure

```
CAD/
├── app.py                      # Main Flask application
├── cad_processor.py            # DXF processing & geometry extraction
├── cost_calculator.py          # Cost & time calculation
├── pdf_generator.py            # PDF quotation generation
├── ai_advisor.py              # AI-powered recommendations
├── path_optimizer.py          # TSP path optimization
├── nesting_optimizer.py       # Material sheet nesting
├── pdf_utils.py               # PDF utility functions
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── branding.json              # Company branding config
│
├── templates/                 # HTML templates
│   ├── index.html            # Home page
│   ├── features.html         # Analysis results page
│   ├── ai_recommendations.html # AI recommendations page
│   ├── about.html            # About page
│   ├── contact.html          # Contact page
│   ├── faq.html              # FAQ page
│   └── pricing.html          # Pricing page
│
├── static/                    # Static assets
│   ├── css/
│   │   └── styles.css        # Custom styles
│   ├── js/
│   │   ├── app.js            # Main JavaScript
│   │   └── path_visualizer.js # Path visualization
│   └── img/
│       └── tech_support_logo.jpg
│
├── uploads/                   # Temporary uploads (auto-created)
├── temp_pdfs/                 # Generated PDFs (auto-created)
│
└── Documentation/
    ├── README.md             # This file
    ├── AI_INTEGRATION_PLAN.md
    ├── LLM_QUICK_WINS.md
    └── SETUP_AI.md
```

---

## 🎓 Learning Resources

### Understanding the Code

**For Beginners:**
1. Start with `app.py` - understand routing
2. Read `cad_processor.py` - see how DXF is parsed
3. Check `cost_calculator.py` - understand cost formulas
4. Explore `pdf_generator.py` - see PDF creation

**For Advanced Users:**
1. Study `path_optimizer.py` - TSP algorithm implementation
2. Review `nesting_optimizer.py` - bin packing algorithm
3. Examine `ai_advisor.py` - AI integration patterns
4. Analyze complexity scoring in `cad_processor.py`

---

## 🚀 Performance Tips

1. **Large Files:** Processing time increases with entity count
2. **AI Features:** First load takes 10-30 seconds, then cached
3. **PDF Generation:** Usually < 2 seconds
4. **Visualizations:** Canvas rendering is optimized for 100-1000 entities

---

## 📞 Support & Contribution

### Getting Help

1. Check this README first
2. Review error messages in console
3. Check browser console for JavaScript errors
4. Verify all dependencies are installed

### Contributing

1. Follow PEP 8 style guidelines
2. Add docstrings to new functions
3. Test thoroughly before submitting
4. Update this README for new features

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **ezdxf**: DXF file processing library
- **ReportLab**: PDF generation capabilities
- **Flask**: Web framework
- **OpenRouter**: Free AI model access
- **Bootstrap**: UI components and styling

---

**Built with ❤️ for the CNC manufacturing community**

*Precision CNC Solutions - Making manufacturing smarter, one quotation at a time.*

---

## 📝 Version History

- **v2.0** - AI integration, path optimization, nesting optimization
- **v1.5** - Professional PDF generation, complexity scoring
- **v1.0** - Initial release with basic DXF processing

---

**Last Updated:** January 2025
