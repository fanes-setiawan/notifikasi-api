from flask import Flask
from app.routes import notification_blueprint

def create_app():
    app = Flask(__name__)

    # Register blueprint
    app.register_blueprint(notification_blueprint, url_prefix="/api/v1/notifications")

    @app.route("/")
    def root():
        return {"message": "Notification API is running"}

    return app
