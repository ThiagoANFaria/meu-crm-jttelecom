"""
Serviço de email do CRM
"""

class EmailService:
    @staticmethod
    def send_email(to_email, subject, body):
        """Envia um email"""
        try:
            # Implementação básica - pode ser expandida com SMTP real
            print(f"📧 Email enviado para {to_email}")
            print(f"Assunto: {subject}")
            print(f"Corpo: {body}")
            
            return {'success': True, 'message': 'Email enviado com sucesso'}
            
        except Exception as e:
            return {'success': False, 'message': f'Erro ao enviar email: {str(e)}'}

