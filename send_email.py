import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from vercel import Request, Response  # Vercel usa esto

SMTP_USER = os.getenv("smtp_user")
SMTP_PASS = os.getenv("smtp_pass")

def handler(request: Request):
    # Health check
    if request.method == "GET":
        return Response({"status": "OK", "message": "Servidor funcionando correctamente"}, status=200)
    
    # POST → enviar correo
    try:
        data = request.json
        nombre = data.get("nombre", "").strip()
        email = data.get("email", "").strip()
        asunto = data.get("asunto", "").strip()
        mensaje = data.get("mensaje", "").strip()

        if not all([nombre, email, asunto, mensaje]):
            return Response({"success": False, "error": "Todos los campos son obligatorios"}, status=400)
        
        fecha_hora = datetime.now().strftime("%d de %B de %Y a las %H:%M")

        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
            <title>Nuevo mensaje - Portafolio Julio</title>
        </head>
        <body style="margin: 0; padding: 0; background-color: #f4f5f7; font-family: 'Inter', sans-serif;">

            <table width="100%" cellpadding="0" cellspacing="0" style="padding: 40px 20px;">
                <tr>
                    <td align="center">

                        <table width="650" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 6px 30px rgba(0,0,0,0.08);">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background-color: #0d6efd; padding: 45px 40px; text-align: center;">
                                    <div style="font-size: 48px; margin-bottom: 10px;">📨</div>
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700;">
                                        Nuevo mensaje desde tu portafolio
                                    </h1>
                                    <p style="margin-top: 8px; color: rgba(255,255,255,0.9); font-size: 15px;">
                                        Recibiste un mensaje de <strong>{nombre}</strong>
                                    </p>
                                    <div style="margin-top: 18px; font-size: 13px; color: rgba(255,255,255,0.9); background: rgba(255,255,255,0.15); display:inline-block; padding: 6px 16px; border-radius: 20px;">
                                        📅 {fecha_hora}
                                    </div>
                                </td>
                            </tr>

                            <!-- Body -->
                            <tr>
                                <td style="padding: 40px 45px; color: #333333;">
                                    
                                    <h2 style="margin-top: 0; color: #0d6efd; font-size: 20px; font-weight: 700;">Información del remitente</h2>
                                    <table width="100%" cellpadding="10" cellspacing="0" style="margin-top: 10px;">
                                        <tr>
                                            <td style="color: #6c757d; font-weight: 600; width: 120px;">👤 Nombre</td>
                                            <td style="font-weight: 600;">{nombre}</td>
                                        </tr>
                                        <tr>
                                            <td style="color: #6c757d; font-weight: 600;">✉️ Email</td>
                                            <td>
                                                <a href="mailto:{email}" style="color: #0d6efd; text-decoration: none;">{email}</a>
                                            </td>
                                        </tr>
                                    </table>

                                    <hr style="border: none; border-top: 1px solid #e9ecef; margin: 30px 0;">

                                    <h3 style="color: #0d6efd; font-size: 18px; font-weight: 700;">Asunto</h3>
                                    <p style="font-size: 16px; font-weight: 500; background: #f8f9fa; border-left: 4px solid #0d6efd; padding: 14px 18px; border-radius: 10px;">
                                        {asunto}
                                    </p>

                                    <h3 style="color: #0d6efd; font-size: 18px; font-weight: 700; margin-top: 30px;">Mensaje</h3>
                                    <div style="background: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 10px; font-size: 15px; line-height: 1.7; color: #333;">
                                        {mensaje}
                                    </div>

                                    <div style="text-align: center; margin-top: 40px;">
                                        <a href="mailto:{email}?subject=Re: {asunto}" 
                                           style="background-color: #0d6efd; color: #fff; text-decoration: none; padding: 14px 30px; border-radius: 8px; font-weight: 600; display: inline-block; transition: 0.3s;">
                                            💬 Responder mensaje
                                        </a>
                                    </div>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f9fa; text-align: center; padding: 25px 20px;">
                                    <p style="margin: 0; color: #6c757d; font-size: 13px;">Este mensaje fue enviado desde el formulario de contacto de tu portafolio Julio.com</p>
                                    <p style="margin: 8px 0 0; color: #adb5bd; font-size: 12px;">© {datetime.now().year} José Julio Sánchez Cruzado | Todos los derechos reservados</p>
                                    <div style="margin-top: 12px;">
                                        <a href="https://linkedin.com/in/josejuliosanchezcruzado" style="color: #0d6efd; text-decoration: none; font-size: 12px; margin: 0 6px;">LinkedIn</a> |
                                        <a href="https://github.com/J0seJuli0" style="color: #0d6efd; text-decoration: none; font-size: 12px; margin: 0 6px;">GitHub</a> |
                                        <a href="https://wa.me/51902027977" style="color: #0d6efd; text-decoration: none; font-size: 12px; margin: 0 6px;">WhatsApp</a>
                                    </div>
                                </td>
                            </tr>
                        </table>

                    </td>
                </tr>
            </table>

        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Nuevo Contacto: {asunto}"
        msg["From"] = f"Julio.com <{SMTP_USER}>"
        msg["To"] = SMTP_USER
        msg["Reply-To"] = email
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return Response({"success": True, "message": "Mensaje enviado correctamente"}, status=200)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
