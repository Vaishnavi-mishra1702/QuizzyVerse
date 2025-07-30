from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.app_context().push()

    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()
celery_app = celery

# ✅ Import your register_routes and register the routes!
from application.routes import register_routes
register_routes(app, db)  # This is missing in your current code

if __name__ == "__main__":
    app.run(debug=True)
