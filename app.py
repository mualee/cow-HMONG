from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import SQLALCHEMY_DATABASE_URI
from models import db, User, Bank
import requests
import json

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'your_secret_key_here'  # Change this to a secure random value
db.init_app(app)

@app.route('/')
def index():
    if 'user_id' in session:
        users = User.query.all()
        banks = Bank.query.filter_by(user_id=session['user_id']).all()
        return render_template('index.html', users=users, banks=banks)
    return redirect(url_for('login'))

@app.route('/add-back', methods=['GET', 'POST'])
def add_bank():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        back_name = request.form['back_name']
        back_code = request.form['back_code']
        back_account = request.form['back_account']
        amount = request.form.get('amount', 0)
        is_active = request.form.get('is_active', 'true') == 'true'
        
        new_bank = Bank(
            back_name=back_name, 
            back_code=back_code, 
            back_account=back_account, 
            amount=float(amount) if amount else 0.0,
            is_active=is_active,
            user_id=str(session['user_id'])  # Ensure it's a string
        )
        db.session.add(new_bank)
        db.session.commit()
        banks = Bank.query.filter_by(user_id=session['user_id']).all()
        flash('Bank account added successfully!')
        return render_template('add_Account.html', banks=back)
    if back := Bank.query.filter_by(user_id=session['user_id']).all():
        # If the user already has bank accounts, render the form with existing accounts
        return render_template('add_Account.html', banks=back)
    else:
        return render_template('add_Account.html')

@app.route('/add-back-account', methods=['POST'])
def add_bank_account():
    if 'user_id' not in session:
        return '', 401
    back_name = request.form['back_name']
    back_code = request.form['back_code']
    back_account = request.form['back_account']
    amount = request.form.get('amount', 0)
    is_active = request.form.get('is_active', 'true') == 'true'
    
    new_bank = Bank(
        back_name=back_name, 
        back_code=back_code, 
        back_account=back_account, 
        amount=float(amount) if amount else 0.0,
        is_active=is_active,
        user_id=str(session['user_id'])  # Ensure it's a string
    )
    db.session.add(new_bank)
    db.session.commit()
    return '', 204  # No content (for HTMX)

@app.route('/add-user', methods=['POST'])
def add_user():
    if 'user_id' not in session:
        return '', 401
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form.get('phone', '')
    # No password for added users here
    new_user = User(
        fristname=firstname, 
        lastname=lastname, 
        email=email, 
        phone=phone,
        passwrod=generate_password_hash('default123'),
        role='user'
    )
    db.session.add(new_user)
    db.session.commit()
    
    # Check if request is HTMX (for AJAX) or regular form submission
    if request.headers.get('HX-Request'):
        return '', 204  # No content for HTMX
    else:
        flash('User added successfully!')
        return redirect(url_for('index'))  # Redirect for regular form submission



# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form.get('phone', '')
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        new_user = User(
            fristname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            passwrod=generate_password_hash(password),
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwrod, password):
            session['user_id'] = str(user.idusers)  # Convert UUID to string
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        flash('Invalid credentials')
        return redirect(url_for('login'))
    return render_template('login.html')

# Topup route
@app.route('/topup', methods=['GET', 'POST'])
def topup():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        bank_id = request.form['bank_id']
        amount = float(request.form['amount'])
        
        bank = Bank.query.filter_by(id=bank_id, user_id=session['user_id']).first()
        if bank:
            bank.amount += amount
            db.session.commit()
            flash(f'Successfully topped up ${amount:.2f} to {bank.back_name}')
        else:
            flash('Bank account not found')
        return redirect(url_for('index'))
    
    banks = Bank.query.filter_by(user_id=session['user_id']).all()
    return render_template('topup.html', banks=banks)

@app.route('/topup_BcelOne', methods=['POST'])
def topup_bcel_one():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        bank_id = request.form['bank_id']
        amount = float(request.form['amount'])
        description = request.form.get('description', 'Bank Account Top Up')
        
        # Validate bank belongs to user
        bank = Bank.query.filter_by(id=bank_id, user_id=session['user_id']).first()
        if not bank:
            flash('Bank account not found')
            return redirect(url_for('topup'))
        
        url = "https://payment-gateway.lailaolab.com/v1/api/payment/generate-bcel-qr"
     
        payload = json.dumps({
            "amount": 1,
            "description": f"test"
        })
        headers = {
            'secretKey': '$2a$10$CsNB00Yssf1HaDz8UDllQOqxU5htsYeo9PU.E/1Q0kphvI6vPu5LC',
            'Content-Type': 'application/json'
        }
     
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data.get('message') == "SUCCESSFULLY":
                qrCode = response_data.get('qrCode')
                link = response_data.get('link')
                
                # Update bank balance
                bank.amount += amount
                db.session.commit()
                
                flash(f'BCEL One payment successful! Added ${amount:.2f} to {bank.back_name}')
                return render_template('topup.html', qrCode=qrCode, link=link, banks=Bank.query.filter_by(user_id=session['user_id']).all())
            else:
                flash(f'Payment failed: {response_data.get("message", "Unknown error")}')
        else:
            flash(f'Payment gateway error: {response.status_code}')
            
    except ValueError:
        flash('Invalid amount entered')
    except requests.RequestException as e:
        flash(f'Network error: {str(e)}')
    except Exception as e:
        flash(f'Error processing payment: {str(e)}')
    
    return redirect(url_for('topup'))


# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
