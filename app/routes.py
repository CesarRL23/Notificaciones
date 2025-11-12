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
    def send_html_email():
        try:
            print("[NOTIFICATION SERVICE] Received HTML email request")
            data = request.get_json()
            print(f"[NOTIFICATION SERVICE] Request data: {data}")
            
            required_fields = ['sender', 'to', 'subject', 'html_content']
            
            if not all(field in data for field in required_fields):
                missing = [field for field in required_fields if field not in data]
                print(f"[NOTIFICATION SERVICE] Missing fields: {missing}")
                return jsonify({"error": f"Missing required fields: {missing}"}), 400

            service = GmailService.get_service()
            print("[NOTIFICATION SERVICE] Gmail service initialized")
            
            message = MessageBuilder.create_html_message(
                sender=data['sender'],
                to=data['to'],
                subject=data['subject'],
                html_content=data['html_content']
            )
            print("[NOTIFICATION SERVICE] Message built successfully")
            
            result = GmailService.send_message(service, 'me', message)
            print(f"[NOTIFICATION SERVICE] Email sent successfully: {result}")
            
            return jsonify(result), 200
        
        except Exception as e:
            print(f"[NOTIFICATION SERVICE] Error sending HTML email: {str(e)}")
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
