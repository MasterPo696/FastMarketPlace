from app.config import db
from app.pictures import ImageHandler
from app.models.product_models import Item, Category, Subcategory

def handle_item_creation(form_data, image_file):
    try:
        title = form_data['title']
        price = float(form_data['price'])
        description = form_data['description']
        weight = float(form_data['weight'])
        subcategory_id = int(form_data['subcategory'])
        
        # Get subcategory and category info for image naming
        subcategory = Subcategory.query.get_or_404(subcategory_id)
        category = subcategory.category
        
        # Generate image filename
        file_extension = image_file.filename.rsplit('.', 1)[1].lower()
        image_filename = f"item_{subcategory.name.lower()}_{category.name.lower()}.{file_extension}"
        
        image_handler = ImageHandler()
        image_path, error, code = image_handler.handle_image_upload(image_file, image_filename)
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
            subcategory_id=subcategory_id
        )

        db.session.add(item)
        db.session.commit()
        
        # Save to items.json
        import json
        import os
        
        items_file = 'static/items.json'
        items_data = {'items': []}
        
        if os.path.exists(items_file):
            with open(items_file, 'r', encoding='utf-8') as f:
                items_data = json.load(f)
        
        items_data['items'].append({
            'id': item.id,
            'title': title,
            'price': price,
            'description': description,
            'image_path': image_path,
            'weight': weight,
            'category': category.name,
            'subcategory': subcategory.name
        })
        
        with open(items_file, 'w', encoding='utf-8') as f:
            json.dump(items_data, f, indent=4, ensure_ascii=False)
            
        return None, None
    except Exception as e:
        return f"Error creating item: {str(e)}", 500

def get_categories():
    return Category.query.all()

def get_subcategories(category_id):
    return Subcategory.query.filter_by(category_id=category_id).all()
