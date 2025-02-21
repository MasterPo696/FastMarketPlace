from app.config import db
from app.pictures import ImageHandler
from app.models import Item, Category, Subcategory

def handle_item_creation(form_data, image_file):
    try:
        title = form_data['title']
        price = float(form_data['price'])
        description = form_data['description']
        weight = float(form_data['weight'])
        subcategory_id = int(form_data['subcategory'])
        
        # Проверяем существование подкатегории
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        
        image_handler = ImageHandler()
        image_path, error, code = image_handler.handle_image_upload(image_file)
        if error:
            return error, code

        item = Item(
            title=title,
            price=price,
            description=description,
            image_path=image_path,
            discount=0,
            weight=weight,
            amount=1,
            isAvailable=True,
            subcategory_id=subcategory_id
        )

        db.session.add(item)
        db.session.commit()
        return None, None
    except Exception as e:
        return f"Error creating item: {str(e)}", 500

def get_categories():
    return Category.query.all()

def get_subcategories(category_id):
    return Subcategory.query.filter_by(category_id=category_id).all()
