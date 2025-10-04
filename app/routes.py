from flask import jsonify, request
from app.services.gmail_service import GmailService
from app.utils.message_builder import MessageBuilder

def init_routes(app):
    @app.before_request
    def check_json():
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({
                    "error": "El Content-Type debe ser application/json",
                    "tip": "Asegúrate de configurar el header Content-Type: application/json en Postman"
                }), 415

    @app.route('/send/plain', methods=['POST'])
    def send_plain_text():
        try:
            data = request.get_json()
            required_fields = ['sender', 'to', 'subject', 'message']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            service = GmailService.get_service()
            
            message = MessageBuilder.create_plain_message(
                sender=data['sender'],
                to=data['to'],
                subject=data['subject'],
                message_text=data['message']
            )
            
            result = GmailService.send_message(service, 'me', message)
            return jsonify(result)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/send/html', methods=['POST'])
    def send_html():
        try:
            data = request.get_json()
            required_fields = ['sender', 'to', 'subject', 'html_content']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            service = GmailService.get_service()
            
            message = MessageBuilder.create_html_message(
                sender=data['sender'],
                to=data['to'],
                subject=data['subject'],
                html_content=data['html_content']
            )
            
            result = GmailService.send_message(service, 'me', message)
            return jsonify(result)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500