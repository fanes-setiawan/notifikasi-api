from app.services.firebase_service import send_firebase_notification

def send_notification_controller(token: str, title: str, body: str, data: dict):
    try:
        response = send_firebase_notification(token, title, body, data)
        return {"status": "success", "data": response}
    except Exception as e:
        raise Exception(f"Error in notification controller: {str(e)}")
