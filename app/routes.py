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

    @app.route('/send/otp', methods=['POST'])
    def send_otp():
        try:
            data = request.get_json()
            required_fields = ['to', 'otp']

            # Validar campos obligatorios
            if not all(field in data for field in required_fields):
                return jsonify({"success": False, "message": "Faltan campos obligatorios"}), 400

            email = data['to']
            otp = data['otp']

        # Preparar contenido del correo
            subject = "🔐 Tu código de verificación - Explavia"
            html_content = f"""
            <html>
                <body>
                    <h2>Tu código de verificación</h2>
                    <p>Usa este código para completar tu verificación:</p>
                    <h3>{otp}</h3>
                    <p>Este código expirará en unos minutos.</p>
                </body>
            </html>
            """

            # Inicializar servicio Gmail
            service = GmailService.get_service()

            # Construir mensaje
            message = MessageBuilder.create_html_message(
                sender="no-reply@explavia.com",
                to=email,
                subject=subject,
                html_content=html_content
            )

            # Enviar correo
            result = GmailService.send_message(service, 'me', message)

            return jsonify({
                "success": True,
                "message": "Código de verificación enviado a tu correo",
                "result": result
            }), 200

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
