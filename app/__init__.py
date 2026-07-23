import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Lấy đường dẫn tuyệt đối tới thư mục 'app'
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        # Chỉ định chính xác vị trí templates và static bên trong thư mục app
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )

    # Cấu hình Database & Config khác của bạn...
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    # Register blueprints (nếu có)...
    # from app.routes.task_routes import main_bp
    # app.register_blueprint(main_bp)

    return app