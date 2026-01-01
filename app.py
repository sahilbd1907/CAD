from flask import Flask, render_template, request, jsonify, send_file, Response, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename
from cad_processor import CADProcessor
from cost_calculator import CostCalculator
from pdf_generator import PDFGenerator
from ai_advisor import AIAdvisor
import tempfile
from pdf_utils import extract_pdf_text

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
cad_processor = CADProcessor()
cost_calculator = CostCalculator()
pdf_generator = PDFGenerator()
ai_advisor = AIAdvisor()
results_cache = {}

# Allowed file extensions
ALLOWED_EXTENSIONS = {'dxf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cnc-cutting')
def cnc_cutting():
    return render_template('cnc_cutting.html')

@app.route('/branding.css')
def branding_css():
    try:
        with open('branding.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        colors = data.get('colors', {})
        css = f":root{{--brand-primary:{colors.get('primary', '#4f46e5')};--brand-secondary:{colors.get('secondary', '#06b6d4')};--brand-accent:{colors.get('accent', '#f43f5e')};--success:{colors.get('success', '#16a34a')};--surface:{colors.get('surface', '#ffffff')};--surface-2:{colors.get('surface2', '#f6f7fb')};--text-strong:{colors.get('textStrong', '#0f172a')};--text-muted:{colors.get('textMuted', '#64748b')};--border:{colors.get('border', '#e2e8f0')};}}"
        return Response(css, mimetype='text/css')
    except Exception:
        return Response(":root{}", mimetype='text/css')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process CAD file
            geometry_data = cad_processor.process_dxf(filepath)
            
            # Get material and thickness from form
            material = request.form.get('material', 'steel')
            thickness = float(request.form.get('thickness', 1.0))
            
            # Calculate costs
            cutting_length = geometry_data['total_length']
            machining_time = cost_calculator.calculate_machining_time(cutting_length, material, thickness)
            total_cost = cost_calculator.calculate_total_cost(machining_time, material, thickness, cutting_length)
            
            # Get AI recommendations (async/non-blocking - can be slow)
            ai_recommendations = None
            try:
                ai_recommendations = ai_advisor.get_recommendations(
                    geometry_data, material, thickness, machining_time, total_cost
                )
            except Exception as e:
                print(f"AI recommendations error (non-critical): {str(e)}")
                # Continue without AI recommendations
            
            # Store results by ID for features page
            result_id = os.path.splitext(filename)[0] + '_' + next(tempfile._get_candidate_names())
            results_cache[result_id] = {
                'geometry': geometry_data,
                'material': material,
                'thickness': thickness,
                'machining_time': machining_time,
                'total_cost': total_cost,
                'ai_recommendations': ai_recommendations
            }

            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'id': result_id
            })
            
        except Exception as e:
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_pdf(filename):
    try:
        return send_file(
            os.path.join('temp_pdfs', filename),
            as_attachment=True,
            download_name=f'cnc_quotation_{filename}'
        )
    except FileNotFoundError:
        return jsonify({'error': 'PDF not found'}), 404

@app.route('/features/<result_id>')
def features(result_id):
    data = results_cache.get(result_id)
    if not data:
        return redirect(url_for('index'))
    return render_template('features.html', result_id=result_id, **data)

@app.route('/ai-recommendations/<result_id>')
def ai_recommendations(result_id):
    """Dedicated page for comprehensive AI recommendations"""
    data = results_cache.get(result_id)
    if not data:
        return redirect(url_for('index'))
    
    # Check if AI data is already cached (from async load or previous request)
    # If not, don't load it here - let it load async for faster page load
    if 'comprehensive_ai' not in data or data.get('comprehensive_ai') is None:
        # Check if this is a reload after AI data was loaded
        if request.args.get('ai_loaded') == 'true' and 'comprehensive_ai' in data:
            # AI data should be cached now, use it
            pass
        else:
            # First load - set to None so async loading happens
            data['comprehensive_ai'] = None
    
    return render_template('ai_recommendations.html', result_id=result_id, **data)

@app.route('/api/ai-analysis/<result_id>')
def get_ai_analysis(result_id):
    """Async endpoint to fetch AI analysis"""
    data = results_cache.get(result_id)
    if not data:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        print(f"Fetching comprehensive AI analysis for {result_id}...")
        comprehensive_ai = ai_advisor.get_comprehensive_ai_analysis(
            data['geometry'],
            data['material'],
            data['thickness'],
            data['machining_time'],
            data['total_cost']
        )
        # Cache the AI data for future page loads
        data['comprehensive_ai'] = comprehensive_ai
        results_cache[result_id] = data
        print(f"AI analysis completed and cached for {result_id}")
        
        return jsonify({
            'success': True,
            'data': comprehensive_ai
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error getting comprehensive AI analysis: {e}")
        print(f"Traceback: {error_details}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tsp-calculate/<result_id>')
def calculate_tsp_path(result_id):
    """Calculate TSP-optimized path"""
    data = results_cache.get(result_id)
    if not data:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        from path_optimizer import PathOptimizer
        optimizer = PathOptimizer()
        tsp_result = optimizer.calculate_tsp_path(data['geometry'])
        return jsonify({
            'success': True,
            'data': tsp_result
        })
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Path optimizer module not found'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nesting-calculate/<result_id>')
def calculate_nesting(result_id):
    """Calculate optimal nesting"""
    data = results_cache.get(result_id)
    if not data:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        from nesting_optimizer import NestingOptimizer
        optimizer = NestingOptimizer()
        nesting_result = optimizer.calculate_optimal_nesting(
            data['geometry'],
            data['material'],
            data['thickness']
        )
        return jsonify({
            'success': True,
            'data': nesting_result
        })
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Nesting optimizer module not found'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate-pdf/<result_id>')
def generate_pdf(result_id):
    data = results_cache.get(result_id)
    if not data:
        return jsonify({'error': 'Not found'}), 404
    filename = pdf_generator.generate_quotation(
        data['geometry'], data['material'], data['thickness'], data['machining_time'], data['total_cost']
    )
    return redirect(url_for('download_pdf', filename=filename))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    brochure_path = 'Brochure_Tech support 2.pdf'
    about_text = ''
    services = []
    try:
        text = extract_pdf_text(brochure_path)
        about_text, services, _ = _extract_brochure_sections(text)
    except Exception:
        pass
    return render_template('about.html', about_text=about_text, services=services)

@app.route('/contact')
def contact():
    brochure_path = 'Brochure_Tech support 2.pdf'
    contact_info = {}
    try:
        text = extract_pdf_text(brochure_path)
        _, _, contact_info = _extract_brochure_sections(text)
    except Exception:
        pass
    return render_template('contact.html', contact=contact_info)

@app.route('/spec')
def spec():
    try:
        text = extract_pdf_text('show_5.pdf')
        return Response(text, mimetype='text/plain')
    except Exception as e:
        return Response(str(e), mimetype='text/plain', status=500)

def _extract_brochure_sections(text: str):
    """
    Very simple brochure parser: splits out About/Services/Contact sections if headings exist.
    Returns: (about_text, services_list, contact_dict)
    """
    lower = text.lower()
    def find_section(start_keys, end_keys):
        start = min((lower.find(k) for k in start_keys if lower.find(k) != -1), default=-1)
        if start == -1:
            return ''
        end_positions = [lower.find(k, start + 1) for k in end_keys]
        end_positions = [p for p in end_positions if p != -1]
        end = min(end_positions) if end_positions else len(text)
        return text[start:end].strip()

    about_text = find_section(['about us', 'about company', 'company profile'], ['services', 'our services', 'contact', 'get in touch'])
    services_text = find_section(['services', 'our services', 'capabilities'], ['contact', 'get in touch', 'about', 'company profile'])
    contact_text = find_section(['contact', 'get in touch', 'reach us'], ['about', 'services'])

    services = []
    for line in services_text.splitlines():
        line_strip = line.strip('•- \t')
        if len(line_strip) > 4 and any(w in line_strip.lower() for w in ['cut', 'cnc', 'laser', 'water', 'fabrication', 'machin', 'plasma']):
            services.append(line_strip)

    contact = {}
    for line in contact_text.splitlines():
        l = line.strip()
        if '@' in l and ' ' not in l:
            contact['email'] = l
        if any(k in l.lower() for k in ['phone', 'mob', 'tel', '+91']):
            contact['phone'] = l
        if any(k in l.lower() for k in ['address', 'pune', 'maharashtra', 'india']) and 'address' not in contact:
            contact['address'] = l

    return about_text, services, contact

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
