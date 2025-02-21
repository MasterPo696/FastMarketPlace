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
            # Получаем все товары без фильтра is_active для отладки
            items = Item.query.order_by(Item.title).all()
            categories = Category.query.all()
            
            # Добавим отладочную информацию
            print("Found items:", [f"{item.title} (active: {item.is_active}, available: {item.isAvailable})" for item in items])
            app.logger.info(f"Found {len(items)} items and {len(categories)} categories")
            
            return render_template(
                'index.html',
                items=items,
                categories=categories,
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
            return render_template(
                'admin/products.html',
                items=items,
                categories=categories,
                datetime=datetime
            )
        except Exception as e:
            app.logger.error(f"Error loading admin products page: {str(e)}")
            flash('Error loading products. Please try again.', 'error')
            return redirect(url_for('index')) 