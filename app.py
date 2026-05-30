from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
# Permitimos explícitamente que tu dominio de Netlify lea las respuestas sin bloqueos de CORS
CORS(app, resources={r"/*": {"origins": "*"}}) 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  
EMISOR_CORREO = "velareescape@gmail.com"        
EMISOR_PASSWORD = "aaygrlrrziutvnvh"  

@app.route('/', methods=['POST'])
@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    # Soporte flexible para recibir datos tanto de formularios como de JSON
    if request.form:
        nombre = request.form.get('nombre')
        correo_cliente = request.form.get('email') or request.form.get('correo')
        asunto = request.form.get('asunto')
        mensaje_cliente = request.form.get('mensaje')
    else:
        datos_json = request.get_json(silent=True) or {}
        nombre = datos_json.get('nombre')
        correo_cliente = datos_json.get('email') or datos_json.get('correo')
        asunto = datos_json.get('asunto')
        mensaje_cliente = datos_json.get('mensaje')

    # Valores por defecto en caso de campos vacíos para evitar que falle la sintaxis de Python
    nombre = nombre if nombre else "Usuario Anónimo"
    correo_cliente = correo_cliente if correo_cliente else "No proporcionado"
    asunto = asunto if asunto else "Sin Asunto"
    mensaje_cliente = mensaje_cliente if mensaje_cliente else "Sin mensaje"

    correo_docente ="Jruiz18@cuc.edu.co" 

    try:
        # Conexión SSL nativa y directa de confianza hacia Gmail
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.login(EMISOR_CORREO, EMISOR_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = EMISOR_CORREO
        msg['To'] = correo_docente
        msg['Subject'] = f"✓ PRUEBA VERIFICABLE: {asunto}"

        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #d4af37; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 10px;">
                        Velaré Escape — Evidencia de Entrega
                    </h2>
                    <p>Hola profe,</p>
                    <p>Este es un correo automatizado enviado exitosamente desde la infraestructura de Vercel.</p>
                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #d4af37; margin: 20px 0;">
                        <p><strong>Remitente:</strong> {nombre}</p>
                        <p><strong>Correo de contacto:</strong> {correo_cliente}</p>
                        <p><strong>Asunto:</strong> {asunto}</p>
                        <p><strong>Mensaje enviado:</strong><br><em>"{mensaje_cliente}"</em></p>
                    </div>
                </div>
            </body>
        </html>
        """
        msg.attach(MIMEText(cuerpo_html, 'html'))

        server.sendmail(EMISOR_CORREO, correo_docente, msg.as_string())
        server.quit()

        return jsonify({"status": "success", "message": "Correo enviado con éxito"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Esto permite probarlo localmente si ejecutas 'python app.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)