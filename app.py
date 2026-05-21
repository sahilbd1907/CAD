from flask import Flask, render_template, request, jsonify, send_file, Response, redirect, url_for, session, flash
import json
import os
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from cad_processor import CADProcessor
from cost_calculator import CostCalculator
from pdf_generator import PDFGenerator
from ai_advisor import AIAdvisor
import tempfile
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars


def _require_env(name: str) -> str:
    value = os.environ.get(name, '').strip()
    if not value:
        raise RuntimeError(
            f"Missing {name} in environment. Copy .env.example to .env and set it."
        )
    return value


def _load_secret_key() -> str:
    key = os.environ.get('SECRET_KEY', '').strip()
    if not key or key == 'change-this-secret-key':
        raise RuntimeError(
            "SECRET_KEY must be set in .env (use a long random string). "
            'Generate one: python -c "import secrets; print(secrets.token_hex(32))"'
        )
    return key


def _load_users() -> dict:
    """Admin login from .env — never commit real passwords to source code."""
    username = _require_env('ADMIN_USERNAME')
    password = _require_env('ADMIN_PASSWORD')
    return {username: generate_password_hash(password)}


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = _load_secret_key()

# MongoDB configuration
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cad_app')
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client.get_database()
calculations_collection = db['calculations']

USERS = _load_users()

def login_required(f):
    """Require a logged-in user for protected routes."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

def is_logged_in():
    """Helper to check if a user is logged in."""
    return 'user_id' in session

@app.context_processor
def inject_user():
    """Make auth info available in all templates (for nav login/logout)."""
    return {
        'is_logged_in': is_logged_in(),
        'current_user': session.get('user_id')
    }

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
    """Root route: if not logged in, go to login; otherwise go to dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')

        pwd_hash = USERS.get(username)
        if pwd_hash and check_password_hash(pwd_hash, password):
            session['user_id'] = username
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'error')

    # If already logged in, go straight to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log out the current user."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page (was previously index)."""
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
            
            # Get material, thickness and quantity from form
            material = request.form.get('material', 'steel')
            thickness = float(request.form.get('thickness', 1.0))
            quantity = int(request.form.get('quantity', 1))
            
            # Calculate costs (per part)
            cutting_length = geometry_data['total_length']
            machining_time = cost_calculator.calculate_machining_time(cutting_length, material, thickness)
            total_cost_per_part = cost_calculator.calculate_total_cost(machining_time, material, thickness, cutting_length)
            total_cost = total_cost_per_part * max(quantity, 1)
            
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
                'quantity': quantity,
                'machining_time': machining_time,
                'total_cost_per_part': total_cost_per_part,
                'total_cost': total_cost,
                'ai_recommendations': ai_recommendations
            }

            # Persist calculation details to MongoDB
            try:
                calculations_collection.insert_one({
                    'result_id': result_id,
                    'cad_filename': filename,
                    'input': {
                        'material': material,
                        'thickness': thickness,
                        'quantity': quantity,
                    },
                    'calculated': {
                        'total_length': cutting_length,
                        'machining_time': machining_time,
                    },
                    'quotation': {
                        'total_cost_per_part': total_cost_per_part,
                        'total_cost': total_cost,
                        'pdf_filename': None,  # will be updated when PDF is generated
                    },
                    'created_at': datetime.utcnow(),
                })
            except Exception as e:
                # Log DB errors but don't block the main flow
                print(f"MongoDB insert error (non-critical): {e}")

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

@app.route('/generate-pdf-from-db/<quote_id>')
@login_required
def generate_pdf_from_db(quote_id):
    """Generate PDF from database values (with updated/edited values)"""
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(quote_id)
    except Exception:
        flash('Invalid quotation ID', 'error')
        return redirect(url_for('history'))
    
    try:
        # Fetch quotation from database
        quotation = calculations_collection.find_one({'_id': obj_id})
        
        if not quotation:
            flash('Quotation not found', 'error')
            return redirect(url_for('history'))
        
        # Extract data from database
        material = quotation.get('input', {}).get('material', 'steel')
        thickness = quotation.get('input', {}).get('thickness', 1.0)
        quantity = quotation.get('input', {}).get('quantity', 1)
        total_length = quotation.get('calculated', {}).get('total_length', 0)
        machining_time = quotation.get('calculated', {}).get('machining_time', 0)
        total_cost = quotation.get('quotation', {}).get('total_cost', 0)
        total_cost_per_part = quotation.get('quotation', {}).get('total_cost_per_part', 0)
        
        # Create minimal geometry_data structure from database values
        # This is needed for PDF generation but we only have total_length stored
        geometry_data = {
            'total_length': total_length,
            'line_count': 0,
            'arc_count': 0,
            'circle_count': 0,
            'polyline_count': 0,
            'spline_count': 0,
            'ellipse_count': 0,
            'bounding_box': {
                'width': 0,
                'height': 0,
                'area': 0
            },
            'layer_stats': {},
            'entities': []
        }
        
        # Generate PDF with updated values (including cost per part)
        filename = pdf_generator.generate_quotation(
            geometry_data,
            material,
            thickness,
            machining_time,
            total_cost,
            quantity,
            total_cost_per_part
        )
        
        # Update MongoDB record with new PDF info
        try:
            calculations_collection.update_one(
                {'_id': obj_id},
                {
                    '$set': {
                        'quotation.pdf_filename': filename,
                        'quotation.pdf_generated_at': datetime.utcnow(),
                    }
                },
            )
        except Exception as e:
            print(f"MongoDB update error (non-critical): {e}")
        
        flash('PDF generated successfully with updated values!', 'success')
        return redirect(url_for('download_pdf', filename=filename))
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('history'))

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
        data['geometry'],
        data['material'],
        data['thickness'],
        data['machining_time'],
        data['total_cost'],
        data.get('quantity', 1)
    )

    # Update MongoDB record with PDF info
    try:
        calculations_collection.update_one(
            {'result_id': result_id},
            {
                '$set': {
                    'quotation.pdf_filename': filename,
                    'quotation.pdf_generated_at': datetime.utcnow(),
                }
            },
        )
    except Exception as e:
        print(f"MongoDB update error (non-critical): {e}")

    return redirect(url_for('download_pdf', filename=filename))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/history')
@login_required
def history():
    """Display all quotations from database"""
    try:
        # Fetch all quotations from MongoDB, sorted by creation date (newest first)
        quotations = list(calculations_collection.find().sort('created_at', -1))
        
        # Convert ObjectId to string for JSON serialization
        for quote in quotations:
            quote['_id'] = str(quote['_id'])
            # Format date for display
            if 'created_at' in quote:
                quote['created_at_formatted'] = quote['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(quote['created_at'], datetime) else str(quote['created_at'])
        
        return render_template('history.html', quotations=quotations)
    except Exception as e:
        flash(f'Error loading quotations: {str(e)}', 'error')
        return render_template('history.html', quotations=[])

@app.route('/delete/<quote_id>', methods=['POST'])
@login_required
def delete_quotation(quote_id):
    """Delete a quotation"""
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(quote_id)
    except Exception:
        flash('Invalid quotation ID', 'error')
        return redirect(url_for('history'))
    
    try:
        # Find the quotation to get PDF filename if it exists
        quotation = calculations_collection.find_one({'_id': obj_id})
        
        if not quotation:
            flash('Quotation not found', 'error')
            return redirect(url_for('history'))
        
        # Delete PDF file if it exists
        pdf_filename = quotation.get('quotation', {}).get('pdf_filename')
        if pdf_filename:
            pdf_path = os.path.join('temp_pdfs', pdf_filename)
            try:
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
            except Exception as e:
                print(f"Error deleting PDF file: {e}")
        
        # Delete from MongoDB
        result = calculations_collection.delete_one({'_id': obj_id})
        
        if result.deleted_count > 0:
            flash('Quotation deleted successfully!', 'success')
        else:
            flash('Quotation not found', 'error')
        
        return redirect(url_for('history'))
    except Exception as e:
        flash(f'Error deleting quotation: {str(e)}', 'error')
        return redirect(url_for('history'))

@app.route('/edit/<quote_id>', methods=['GET', 'POST'])
@login_required
def edit_quotation(quote_id):
    """Edit a quotation"""
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(quote_id)
    except Exception:
        flash('Invalid quotation ID', 'error')
        return redirect(url_for('history'))
    
    if request.method == 'POST':
        try:
            # Get form data
            material = request.form.get('material', '').strip()
            thickness = float(request.form.get('thickness', 0))
            quantity = int(request.form.get('quantity', 1))
            total_cost_per_part = float(request.form.get('total_cost_per_part', 0))
            total_cost = float(request.form.get('total_cost', 0))
            
            # Recalculate if needed (optional - you can skip recalculation and just update values)
            # For now, we'll just update the stored values
            update_data = {
                'input.material': material,
                'input.thickness': thickness,
                'input.quantity': quantity,
                'quotation.total_cost_per_part': total_cost_per_part,
                'quotation.total_cost': total_cost,
                'updated_at': datetime.utcnow()
            }
            
            # Update in MongoDB
            result = calculations_collection.update_one(
                {'_id': obj_id},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                flash('Quotation updated successfully!', 'success')
            else:
                flash('No changes made or quotation not found', 'warning')
            
            return redirect(url_for('history'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error updating quotation: {str(e)}', 'error')
    
    # GET request - show edit form
    try:
        quotation = calculations_collection.find_one({'_id': obj_id})
        if not quotation:
            flash('Quotation not found', 'error')
            return redirect(url_for('history'))
        
        # Convert ObjectId to string
        quotation['_id'] = str(quotation['_id'])
        
        # Format date
        if 'created_at' in quotation:
            quotation['created_at_formatted'] = quotation['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(quotation['created_at'], datetime) else str(quotation['created_at'])
        
        return render_template('edit_quotation.html', quotation=quotation)
    except Exception as e:
        flash(f'Error loading quotation: {str(e)}', 'error')
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000 , use_reloader=False)
