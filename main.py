from app import app, db
from app.controllers.init_controller import InitController
from app.routes import register_routes

# Register all routes
register_routes()

if __name__ == '__main__':
    # Create application context
    with app.app_context():
        # Initialize databases and create tables
        db.create_all()
        
        # Initialize admin user and test data
        InitController.init_admin()
        InitController.add_test_product()
    
    # Run the application
    app.run(debug=True)