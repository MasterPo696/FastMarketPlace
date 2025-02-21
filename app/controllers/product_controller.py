from flask import render_template, request, redirect, flash, url_for, jsonify
from app.models.product_models import Item, Category, Subcategory
from app.auth import admin_required, login_required
from app.creation import handle_item_creation
from app.services.image_service import ImageService
from app.config import db, app
from datetime import datetime

class ProductController:
    @staticmethod
    def index():
        """Display homepage"""
        try:
            category_id = request.args.get('category_id', type=int)
            subcategory_id = request.args.get('subcategory_id', type=int)
            
            # Базовый запрос
            query = Item.query.filter_by(is_active=True)
            
            # Применяем фильтры
            if category_id:
                query = query.join(Subcategory).join(Category).filter(Category.id == category_id)
            elif subcategory_id:
                query = query.filter(Item.subcategory_id == subcategory_id)
            
            items = query.order_by(Item.title).all()
            categories = Category.query.all()
            
            return render_template(
                'index.html',
                items=items,
                categories=categories,
                current_category_id=category_id,
                current_subcategory_id=subcategory_id,
                title="Home",
                datetime=datetime
            )
        except Exception as e:
            app.logger.error(f"Error loading index page: {str(e)}")
            flash('Error loading products. Please try again.', 'error')
            return redirect(url_for('index'))

    @staticmethod
    @login_required
    @admin_required
    def create():
        """Create new product page"""
        categories = Category.query.all()
        return render_template('admin/create_product.html', categories=categories)

    @staticmethod
    @login_required
    @admin_required
    def delete_product(product_id):
        """Delete product by ID"""
        try:
            item = Item.query.get_or_404(product_id)
            db.session.delete(item)
            db.session.commit()
            flash('Product deleted successfully', 'success')
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting product: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    @login_required
    @admin_required
    def edit_product(product_id):
        """Edit product by ID"""
        item = Item.query.get_or_404(product_id)
        
        if request.method == 'POST':
            try:
                item.title = request.form['title']
                item.description = request.form['description']
                item.price = float(request.form['price'])
                item.discount = int(request.form['discount'])
                item.weight = float(request.form['weight'])
                item.amount = int(request.form['amount'])
                item.subcategory_id = int(request.form['subcategory_id'])
                
                if 'image' in request.files and request.files['image'].filename:
                    image_path, error, code = ImageService.save_image(request.files['image'])
                    if error:
                        flash(error, 'error')
                        return redirect(url_for('edit_product', product_id=product_id))
                    item.image_path = image_path
                
                db.session.commit()
                flash('Product updated successfully', 'success')
                return redirect(url_for('admin_products'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating product: {str(e)}', 'error')
                return redirect(url_for('edit_product', product_id=product_id))
        
        categories = Category.query.all()
        return render_template(
            'admin/edit_product.html',
            item=item,
            categories=categories
        )

    @staticmethod
    @login_required
    @admin_required
    def admin_products():
        """Display admin products page"""
        try:
            items = Item.query.order_by(Item.title).all()
            categories = Category.query.all()
            
            # Добавляем отладочную информацию
            print(f"Found {len(items)} items in admin_products")
            for item in items:
                print(f"Item: {item.title} (ID: {item.id}, Active: {item.is_active}, Available: {item.isAvailable})")
            
            return render_template(
                'admin/products.html',
                items=items,
                categories=categories,
                title="Admin - Products"
            )
        except Exception as e:
            app.logger.error(f"Error in admin_products: {str(e)}")
            flash('Error loading products', 'error')
            return redirect(url_for('index'))

    @staticmethod
    @login_required
    @admin_required
    def update_stock(product_id):
        """Update product stock"""
        try:
            item = Item.query.get_or_404(product_id)
            data = request.get_json()
            quantity = data.get('quantity', 0)
            
            if quantity > 0:
                item.amount += quantity
                db.session.commit()
                return jsonify({'success': True})
            return jsonify({'success': False, 'error': 'Invalid quantity'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    @login_required
    @admin_required
    def toggle_active(product_id):
        """Toggle product active status"""
        try:
            item = Item.query.get_or_404(product_id)
            item.is_active = not item.is_active
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    @login_required
    @admin_required
    def create_product():
        """Create new product"""
        if request.method == 'POST':
            try:
                # Получаем данные из формы
                title = request.form['title']
                description = request.form['description']
                price = float(request.form['price'])
                discount = int(request.form['discount'])
                weight = float(request.form['weight'])
                amount = int(request.form['amount'])
                subcategory_id = int(request.form['subcategory_id'])
                
                # Обработка изображения
                if 'image' not in request.files:
                    flash('No image uploaded', 'error')
                    return redirect(request.url)
                    
                image = request.files['image']
                if image.filename == '':
                    flash('No image selected', 'error')
                    return redirect(request.url)
                    
                image_path, error, code = ImageService.save_image(image)
                if error:
                    flash(error, 'error')
                    return redirect(request.url)
                
                # Создаем новый товар
                new_item = Item(
                    title=title,
                    description=description,
                    price=price,
                    discount=discount,
                    weight=weight,
                    amount=amount,
                    subcategory_id=subcategory_id,
                    image_path=image_path,
                    is_active=True
                )
                
                db.session.add(new_item)
                db.session.commit()
                
                flash('Product created successfully', 'success')
                return redirect(url_for('admin_products'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating product: {str(e)}', 'error')
                return redirect(url_for('create_product'))
        
        # GET request - показываем форму
        categories = Category.query.all()
        return render_template('admin/create_product.html', categories=categories) 