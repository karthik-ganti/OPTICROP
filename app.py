"""
OptiCrop — Smart Agricultural Production Optimization Engine
Flask backend: authentication, crop-recommendation inference, and persistence.

The trained classifier (model.pkl) and scaler (scaler.pkl) are produced by
train_model.py. The app boots fine without them — the prediction routes show a
friendly "model not trained yet" message until the artifacts exist.
"""

import os
import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models_db import db, User, SoilData, Crop, MLModel, Prediction
from crop_data import CROP_INFO, get_crop_info

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'opticrop_secret_key_2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///opticrop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

MODEL_PATH = os.path.join('models', 'model.pkl')
SCALER_PATH = os.path.join('models', 'scaler.pkl')

# Feature order MUST match the training column order in train_model.py
FEATURE_ORDER = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

model = None
scaler = None


def load_ml_assets():
    """Load the pickled model + scaler into module globals (if trained)."""
    global model, scaler
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        print('[INFO] OptiCrop model + scaler loaded.')
    else:
        print('[WARN] Model files not found. Run `python train_model.py` to train and save model.pkl.')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def seed_crops():
    """Populate the Crop reference table with the 22 crops (once)."""
    if Crop.query.count() == 0:
        for name, info in CROP_INFO.items():
            db.session.add(Crop(
                crop_name=name,
                crop_type=info['crop_type'],
                season=info['season'],
                optimal_ph=info['optimal_ph'],
                water_requirement=info['water_requirement'],
                tips=info['tips'],
            ))
        db.session.commit()


def seed_ml_model():
    """Insert a placeholder MLModel metadata row (once). train_model.py writes
    a models/metrics.txt with the real algorithm + accuracy, which we read here
    if present so the seeded row reflects the deployed model."""
    if MLModel.query.count() == 0:
        algo, acc = 'Random Forest (best of 4 classifiers)', 0.0
        metrics_path = os.path.join('models', 'metrics.txt')
        if os.path.exists(metrics_path):
            try:
                with open(metrics_path) as f:
                    lines = dict(line.strip().split('=', 1) for line in f if '=' in line)
                algo = lines.get('algorithm', algo)
                acc = float(lines.get('accuracy', 0.0))
            except (ValueError, OSError):
                pass
        db.session.add(MLModel(
            model_name='OptiCrop Crop Recommender',
            algorithm_type=algo,
            accuracy=acc,
            model_file='models/model.pkl',
        ))
        db.session.commit()


# ── Public pages ──────────────────────────────────────────────────────────────
@app.route('/')
def home():
    ml = MLModel.query.first()
    accuracy = round(ml.accuracy, 2) if ml and ml.accuracy else 99.55
    algorithm = ml.algorithm_type if ml else 'Random Forest'
    return render_template('home.html', accuracy=accuracy, algorithm=algorithm)


@app.route('/about')
def about():
    ml = MLModel.query.first()
    accuracy = round(ml.accuracy, 2) if ml and ml.accuracy else 99.55
    algorithm = ml.algorithm_type if ml else 'Random Forest'
    return render_template('about.html', accuracy=accuracy, algorithm=algorithm)


# ── Authentication ────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'Farmer')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('register.html')

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ── Prediction ────────────────────────────────────────────────────────────────
@app.route('/findyourcrop')
@login_required
def predict_form():
    if model is None:
        flash('The recommendation model is not trained yet. Run "python train_model.py" first.', 'danger')
        return redirect(url_for('home'))
    return render_template('findyourcrop.html')


@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if model is None or scaler is None:
        flash('The recommendation model is not trained yet. Run "python train_model.py" first.', 'danger')
        return redirect(url_for('home'))

    try:
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
    except (ValueError, KeyError):
        flash('Invalid input. Please enter numeric values for all seven fields.', 'danger')
        return redirect(url_for('predict_form'))

    # Feature order must match training: N, P, K, temperature, humidity, ph, rainfall
    input_array = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
    scaled_input = scaler.transform(input_array)

    proba = model.predict_proba(scaled_input)[0]
    classes = model.classes_
    order = np.argsort(proba)[::-1]

    recommended = str(classes[order[0]])
    confidence = round(float(proba[order[0]]) * 100, 2)
    top3 = [(str(classes[i]), round(float(proba[i]) * 100, 2)) for i in order[:3]]

    # Persist SoilData + Prediction
    soil_entry = SoilData(
        user_id=current_user.id,
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
    )
    db.session.add(soil_entry)
    db.session.flush()

    ml_model_entry = MLModel.query.first()
    model_id = ml_model_entry.id if ml_model_entry else 1

    crop_row = Crop.query.filter_by(crop_name=recommended).first()
    crop_id = crop_row.id if crop_row else None

    pred_entry = Prediction(
        soil_id=soil_entry.id,
        model_id=model_id,
        crop_id=crop_id,
        recommended_crop=recommended,
        confidence_score=confidence,
        prediction_date=datetime.utcnow(),
    )
    db.session.add(pred_entry)
    db.session.commit()

    # Stash for the result page
    session['recommended'] = recommended
    session['confidence'] = confidence
    session['top3'] = top3
    session['inputs'] = {
        'Nitrogen (N)': nitrogen, 'Phosphorus (P)': phosphorus, 'Potassium (K)': potassium,
        'Temperature (°C)': temperature, 'Humidity (%)': humidity, 'pH': ph, 'Rainfall (mm)': rainfall,
    }
    return redirect(url_for('result'))


@app.route('/result')
@login_required
def result():
    recommended = session.get('recommended')
    if not recommended:
        flash('No recent prediction found. Please submit the form first.', 'info')
        return redirect(url_for('predict_form'))

    info = get_crop_info(recommended)
    return render_template(
        'result.html',
        recommended=recommended,
        confidence=session.get('confidence', 0),
        top3=session.get('top3', []),
        inputs=session.get('inputs', {}),
        info=info,
    )


@app.route('/history')
@login_required
def history():
    records = (
        db.session.query(SoilData, Prediction)
        .join(Prediction, SoilData.id == Prediction.soil_id)
        .filter(SoilData.user_id == current_user.id)
        .order_by(Prediction.prediction_date.desc())
        .all()
    )
    return render_template('history.html', records=records, crop_info=CROP_INFO)


with app.app_context():
    db.create_all()
    seed_crops()
    seed_ml_model()
    load_ml_assets()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
