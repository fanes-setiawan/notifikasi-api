from flask import Blueprint, request, jsonify
from app.controllers.notification_controller import send_notification_controller

notification_blueprint = Blueprint("notifications", __name__)

@notification_blueprint.route("/send-notification", methods=["POST"])
def send_notification():
    try:
        data = request.json
        token = data.get("token")
        title = data.get("title")
        body = data.get("body")
        extra_data = data.get("data", {"key1": "default_value1", "key2": "default_value2"})

        if not token or not title or not body:
            return jsonify({"error": "Token, title, and body are required"}), 400

        response = send_notification_controller(token, title, body, extra_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
