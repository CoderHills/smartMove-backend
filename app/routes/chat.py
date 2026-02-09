from flask import Blueprint, request
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required

chat_bp = Blueprint('chat', __name__, url_prefix='/chats')

@chat_bp.route('', methods=['POST'])
@jwt_required
def create_chat_session(current_user):
    """
    Starts a new chat session.
    """
    # In a real application, you'd create a new chat session record in the database.
    # For now, this is a placeholder.
    data = request.get_json()
    
    # Validate request data
    if not data or 'recipient_id' not in data:
        return error_response("Recipient ID is required.", 400)
        
    recipient_id = data['recipient_id']
    
    # Placeholder logic to create a chat session
    chat_session = {
        "chat_session_id": "some_unique_id",
        "participants": [current_user.id, recipient_id],
        "created_at": "timestamp"
    }
    
    return success(chat_session, 201)

@chat_bp.route('/<string:chat_session_id>/messages', methods=['POST'])
@jwt_required
def send_message(current_user, chat_session_id):
    """
    Sends a message within a chat session.
    """
    data = request.get_json()
    
    # Validate request data
    if not data or 'message_body' not in data:
        return error_response("Message body is required.", 400)
    
    message_body = data['message_body']
    
    # Placeholder logic to send a message
    message = {
        "message_id": "another_unique_id",
        "chat_session_id": chat_session_id,
        "sender_id": current_user.id,
        "message_body": message_body,
        "sent_at": "timestamp"
    }

    return success(message, 201)
