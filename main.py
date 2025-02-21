from app import create_app, db
from app.controllers.init_controller import InitController

# Создаем приложение
app = create_app()

def init_app():
    """Initialize the application"""
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Инициализируем админа
        InitController.init_admin()
        
        # Проверяем и заполняем базу данных начальными товарами
        InitController.check_and_fill_database()

if __name__ == '__main__':
    # Инициализация приложения
    init_app()
    
    # Запуск сервера
    app.run(debug=True)