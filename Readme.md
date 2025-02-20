# 🛍️ Flask E-commerce Marketplace

A modern e-commerce marketplace built with Flask, SQLAlchemy, and Bootstrap. Features secure payment processing and image handling capabilities.

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

The following dependencies are required (referenced from):

```1:9:requirements.txt
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

1. Clone the repository:
```bash
git clone https://github.com/MasterPo696/FastMarketPlace.git
cd flask-marketplace
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `secrets/config.toml` with your payment credentials:
```toml
public = 'your_public_key'
secret = 'your_secret_key'
```

5. Initialize the database:
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
│   ├── payments.py      # Payment processing
│   ├── config.py        # Configuration
│   └── pictures.py      # Image handling
├── static/
│   └── images/          # Uploaded product images
├── templates/           # HTML templates
│   ├── index.html       # Main page
│   ├── about.html       # About page
│   ├── create.html      # Create page
│   ├── payment.html     # Payment page
│   └── index.html        # Base template
├── secrets/
│   ├── example.toml      # Configuration files
│   └── config.toml      # Configuration files
├── venv/
├── .gitignore
├── Readme.md
├── main.py             # Application entry point
└── requirements.txt    # Project dependencies
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
The product database structure (referenced from):

```16:25:main.py
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))  # Add this line

    def __repr__(self):
        return f'{self.title}'
```


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
