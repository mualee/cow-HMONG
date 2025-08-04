# Flask Bank Management System with BCEL One Payment

A Flask-based web application for bank account management with integrated BCEL One payment gateway support.

## Features

- 🔐 **User Authentication**: Registration, login, and logout functionality
- 🏦 **Bank Account Management**: Add, view, and manage bank accounts
- 💰 **Balance Top-up**: Manual balance addition and BCEL One payment integration
- 📱 **Responsive UI**: Bootstrap 5 with modern, mobile-friendly design
- ⚡ **Dynamic Interactions**: HTMX for seamless user experience
- 🔗 **PostgreSQL Integration**: Robust database connectivity

## Tech Stack

- **Backend**: Python 3.12, Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: HTML5, Bootstrap 5, HTMX, Jinja2
- **Payment**: BCEL One API integration
- **Security**: Werkzeug password hashing

## Project Structure

```
cow-hmong/
├── app.py                 # Main Flask application
├── config.py             # Database configuration
├── models.py             # Database models (User, Bank)
├── requirements.txt      # Python dependencies
├── update_schema.sql     # Database schema updates
├── templates/            # HTML templates
│   ├── index.html        # Dashboard
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── topup.html        # Top-up with BCEL payment
│   └── add_Account.html  # Bank account management
└── .gitignore           # Git ignore rules
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd cow-hmong
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   - Ensure PostgreSQL is running
   - Update database connection in `config.py` if needed
   - Run the application to auto-create tables

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## Environment Variables

Create a `.env` file for sensitive configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database
BCEL_API_ENDPOINT=your-bcel-api-endpoint
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)

### Banks Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `back_name` (String) - Bank name
- `back_code` (String) - Account number
- `back_account` (String) - Account name
- `amount` (Decimal) - Current balance
- `is_active` (Boolean)
- `created_at` (DateTime)

## API Endpoints

### Authentication
- `GET /` - Dashboard (requires login)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /register` - Registration page
- `POST /register` - Process registration
- `GET /logout` - Logout

### Bank Management
- `GET /add-Account` - Bank account management page
- `POST /add-back` - Add new bank account

### Payment System
- `GET /topup` - Top-up page
- `POST /topup` - Manual top-up
- `POST /topup_BcelOne` - BCEL One payment integration

## BCEL One Integration

The application supports BCEL One mobile payment with:
- QR code generation for payments
- Direct payment links
- Automatic balance updates
- Error handling and user feedback

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection ready
- SQL injection prevention via SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository.

---

**Note**: This application is designed for educational and demonstration purposes. Ensure proper security measures are implemented before production deployment.
