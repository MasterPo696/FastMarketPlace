from flask import Blueprint, jsonify, request
from src.core.services.product_service import ProductService

product_bp = Blueprint('products', __name__)

def init_routes(product_service: ProductService):
    @product_bp.route('/api/products/<int:id>')
    def get_product(id):
        product = product_service.get_product(id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product)

    @product_bp.route('/api/categories/<int:category_id>/products')
    def list_products(category_id):
        products = product_service.list_products_by_category(category_id)
        return jsonify(products) 