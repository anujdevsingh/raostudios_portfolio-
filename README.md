# Rao Studios Portfolio

<div align="center">
  <img src="https://img.shields.io/badge/Flask-3.1.0-blue" alt="Flask Version" />
  <img src="https://img.shields.io/badge/Python-3.x-green" alt="Python Version" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status" />
</div>

## 📋 Overview

A modern, responsive portfolio website built with Flask. This application showcases professional work, skills, and provides contact functionality.
you can check the website on https://raostudios.co.in/
## ✨ Features

- **Responsive Design** - Looks great on all devices
- **Portfolio Showcase** - Display your work with a modern UI
- **Contact Form** - Integrated email functionality
- **Clean Architecture** - Organized Flask application structure

## 📅 Booking System

The booking page is designed to match the sleek aesthetic of the main site while providing a seamless experience for clients.

### Booking Form Fields

- **Name** - Client's full name
- **Phone Number** - For direct contact
- **Event Type** - Options include Wedding, Pre-Wedding, Haldi, etc.
- **Event Duration** - Start and end dates
- **Address** - Location of the event
- **Additional Notes** - Any special requirements or information

### Payment Processing

- **Token Amount**: ₹500 (non-refundable)
- **Payment Gateway**: Integrated Razorpay for secure Indian transactions
- **Confirmation**: Automated email/SMS to client upon successful booking

## 🚀 Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/raostudios_portfolio.git
   cd raostudios_portfolio
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables**
   ```bash
   # Windows (PowerShell)
   $env:SESSION_SECRET = "your-secret-key"
   $env:MAIL_USERNAME = "your-email@gmail.com"
   $env:MAIL_PASSWORD = "your-email-password"
   $env:MAIL_DEFAULT_SENDER = "your-email@gmail.com"
   
   # macOS/Linux
   export SESSION_SECRET="your-secret-key"
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-email-password"
   export MAIL_DEFAULT_SENDER="your-email@gmail.com"
   ```

## 🏃‍♂️ Running the Application

### Development Mode

```bash
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

### Production Mode

```bash
gunicorn app:app
```

## 🧰 Project Structure

```
raostudios_portfolio/
├── app.py                  # Application configuration
├── extensions.py           # Flask extensions
├── forms.py                # Form definitions 
├── models.py               # Data models
├── routes.py               # URL route definitions
├── requirements.txt        # Dependencies
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # Jinja2 templates
│   ├── base.html           # Base template
│   ├── index.html          # Main page template
│   └── includes/           # Reusable template components
└── venv/                   # Virtual environment (not tracked)
```

## 🛡️ Environment Variables

| Variable | Description |
|----------|-------------|
| SESSION_SECRET | Secret key for session security |
| MAIL_USERNAME | Email account username |
| MAIL_PASSWORD | Email account password |
| MAIL_DEFAULT_SENDER | Default sender email |

## 📝 License

[MIT License](LICENSE)

---

<div align="center">
  <p>Made with ❤️ by Anuj Dev Singh</p>
</div>