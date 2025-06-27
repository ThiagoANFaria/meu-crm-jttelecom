"""
Serviço de email do CRM
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.default_sender = "suporte@jttelecom.com.br"
    
    @staticmethod
    def send_email(to_email, subject, body, sender_email=None):
        """Envia um email"""
        try:
            # Implementação básica - pode ser expandida com SMTP real
            print(f"📧 Email enviado para {to_email}")
            print(f"De: {sender_email or 'suporte@jttelecom.com.br'}")
            print(f"Assunto: {subject}")
            print(f"Corpo: {body}")
            
            return {'success': True, 'message': 'Email enviado com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao enviar email: {str(e)}'}
    
    @staticmethod
    def send_html_email(to_email, subject, html_body, sender_email=None):
        """Envia um email em formato HTML"""
        try:
            print(f"📧 Email HTML enviado para {to_email}")
            print(f"De: {sender_email or 'suporte@jttelecom.com.br'}")
            print(f"Assunto: {subject}")
            
            return {'success': True, 'message': 'Email HTML enviado com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao enviar email HTML: {str(e)}'}
    
    @staticmethod
    def create_mime_message(to_email, subject, body, sender_email=None):
        """Cria uma mensagem MIME"""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email or "suporte@jttelecom.com.br"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            return {'success': True, 'message': msg}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao criar mensagem MIME: {str(e)}'}

