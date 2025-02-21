from app.init_app import init_app
from app.routes import register_routes
from app.controllers.init_controller import InitController

# Initialize the application
app = init_app()

# Register all routes
register_routes()

if __name__ == '__main__':
    # Create application context
    with app.app_context():
        # Initialize admin user and test data
        InitController.init_admin()
        InitController.add_test_product()
    
    # Run the application
    app.run(debug=True)