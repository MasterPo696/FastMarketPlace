from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from toml import load
from app.payments import ProcessPayment
from app.pictures import ImageHandler


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
db = SQLAlchemy(app=app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))  # Add this line

    def __repr__(self):
        return f'{self.title}'
    

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data=items)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/buy/<int:id>')
def buy(id):
    try:
        item = Item.query.get_or_404(id)
        payment_processor = ProcessPayment(item)
        return payment_processor.process_payment(id)
    except Exception as e:
        app.logger.error(f"Payment error: {str(e)}")
        return "Payment error occurred", 500

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        
        # Handle image upload
        if 'image' not in request.files:
            return "No image file provided", 400
        
        image_handler = ImageHandler()
        image_path, error, code = image_handler.handle_image_upload(request.files['image'])
        if error:
            return error, code

        item = Item(
            title=title,
            price=price,
            description=description,
            image_path=image_path
        )

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error adding item to database: {str(e)}", 500
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)