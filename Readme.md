# 🛍️ Flask E-commerce Marketplace

A modern e-commerce marketplace built with Flask, SQLAlchemy, and Bootstrap. This platform offers secure payment processing, image handling capabilities, and a robust product management system.

## ✨ Features

- 📱 Responsive design using Bootstrap 5
- 🌓 Dark/Light theme toggle
- 🖼️ Image upload for products
- 💳 Secure payment processing
- 📦 Product management system
- 🔐 Secure file handling
- 🗄️ SQLite database integration
  

## 🛠️ Technologies Used

- Flask
- Flask-SQLAlchemy
- Bootstrap 5
- Python-Magic
- Pillow
- SQLite
- TOML

## 📋 Prerequisites

Ensure you have the following dependencies installed:

```plaintext
flask
flask-sqlalchemy
toml
requests
json
datetime
hashlib
Pillow
python-magic
```

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MasterPo696/FastMarketPlace.git
   cd flask-marketplace
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `secrets/config.toml` with your payment credentials:**

   ```toml
   public = 'your_public_key'
   secret = 'your_secret_key'
   ```

5. **Initialize the database:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## 🏃‍♂️ Running the Application

```bash
python main.py
```

Visit `http://localhost:5000` in your browser.

## 🏗️ Project Structure

```
flask-marketplace/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── services/
│   ├── payments.py      # Payment processing
│   ├── config.py        # Configuration
│   ├── pictures.py      # Image handling
│   ├── routes.py        # Routes
│   └── utils.py         # Utility functions
├── src/
│   ├── core/            # Core functionality   
│   ├── infrastructure/  # Infrastructure
│   └── web/             # Web functionality
├── static/
│   ├── js/              # JavaScript files
│   ├── images/          # Uploaded product images
│   └── json             # JSON files
├── templates/           # HTML templates
│   ├── index.html       # Main page
│   ├── about.html       # About page
│   ├── create.html      # Create page
│   ├── payment.html     # Payment page
│   └── base.html        # Base template
├── secrets/
│   ├── example.toml     # Configuration files
│   └── config.toml      # Configuration files
├── instance/
│   ├── config.toml      # Configuration files
│   └── data.db          # Database
├── venv/
├── .gitignore
├── Readme.md
├── migrations.py        # Migrations
├── main.py              # Application entry point
└── requirements.txt     # Project dependencies
```

## 💡 Key Features Explained

### Payment Processing

The application implements secure payment processing using a third-party payment gateway. The payment system:
- Generates unique order IDs
- Creates secure payment signatures
- Handles payment form generation
- Processes transactions securely

### Image Handling

Secure image upload system with:
- File type validation
- Secure filename generation
- MIME type checking
- Automated directory management

### Database Schema

The product database structure is defined in the `main.py` file.

## 🔐 Security Features

- Secure file upload validation
- Payment signature generation
- MIME type checking
- Secure filename handling
- Error logging
- Exception handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap for the UI components
- Flask community for the excellent documentation
- All contributors who help improve this project

## 📈 Future Enhancements

- Implement a recommendation system for products
- Add support for multiple languages
- Integrate with more payment gateways
- Enhance the admin dashboard with analytics
