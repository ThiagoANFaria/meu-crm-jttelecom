#!/usr/bin/env python3
"""
Script para popular dados iniciais no banco de dados do CRM
"""
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, Role, Permission
from src.models.lead import Tag, LeadFieldTemplate
from src.models.pipeline import Product
from src.models.proposal import ProposalTemplate
from src.models.contract import ContractTemplate
from src.models.chatbot import ChatFlow, ChatAIConfig
from src.models.telephony import TelephonyCall
from flask import Flask

# Configure Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crm_user:crm_password@localhost/crm_jttelcom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def populate_tags():
    """Create default tags."""
    with app.app_context():
        # Check if tags already exist
        if Tag.query.first():
            print("Tags already exist in database.")
            return
        
        default_tags = [
            ('VIP', '#FFD700', 'Cliente VIP'),
            ('Grande Empresa', '#FF6B6B', 'Empresa de grande porte'),
            ('Startup', '#4ECDC4', 'Empresa startup'),
            ('Urgente', '#FF4757', 'Lead com urgência'),
            ('Qualificado', '#2ED573', 'Lead qualificado'),
            ('Frio', '#74B9FF', 'Lead frio'),
            ('Quente', '#FD79A8', 'Lead quente'),
            ('Retomar', '#FDCB6E', 'Retomar contato'),
        ]
        
        for name, color, description in default_tags:
            tag = Tag(name=name, color=color, description=description)
            db.session.add(tag)
        
        db.session.commit()
        print(f"Created {len(default_tags)} default tags.")

def populate_field_templates():
    """Create default field templates."""
    with app.app_context():
        # Check if templates already exist
        if LeadFieldTemplate.query.first():
            print("Field templates already exist in database.")
            return
        
        default_field_templates = [
            ('website', 'Website da Empresa', 'text', None, False, None, 'URL do website da empresa'),
            ('linkedin', 'LinkedIn', 'text', None, False, None, 'Perfil do LinkedIn'),
            ('annual_revenue', 'Faturamento Anual', 'select', ['Até R$ 100k', 'R$ 100k - R$ 500k', 'R$ 500k - R$ 1M', 'R$ 1M - R$ 5M', 'Acima de R$ 5M'], False, None, 'Faturamento anual estimado'),
            ('employees_count', 'Número de Funcionários', 'select', ['1-10', '11-50', '51-200', '201-500', '500+'], False, None, 'Quantidade de funcionários'),
            ('industry', 'Setor/Indústria', 'text', None, False, None, 'Setor de atuação da empresa'),
            ('budget', 'Orçamento Disponível', 'text', None, False, None, 'Orçamento disponível para o projeto'),
            ('decision_timeline', 'Prazo para Decisão', 'select', ['Imediato', '1-3 meses', '3-6 meses', '6-12 meses', 'Mais de 1 ano'], False, None, 'Prazo estimado para tomada de decisão'),
            ('current_solution', 'Solução Atual', 'textarea', None, False, None, 'Solução atualmente utilizada'),
            ('pain_points', 'Principais Dores', 'textarea', None, False, None, 'Principais problemas enfrentados'),
            ('referral_source', 'Fonte da Indicação', 'text', None, False, None, 'Quem indicou ou como chegou até nós'),
        ]
        
        for name, label, field_type, options, is_required, default_value, description in default_field_templates:
            template = LeadFieldTemplate(
                name=name,
                label=label,
                field_type=field_type,
                options=options,
                is_required=is_required,
                default_value=default_value,
                description=description
            )
            db.session.add(template)
        
        db.session.commit()
        print(f"Created {len(default_field_templates)} default field templates.")

def populate_products():
    """Create default products."""
    with app.app_context():
        # Check if products already exist
        if Product.query.first():
            print("Products already exist in database.")
            return
        
        default_products = [
            ("Pabx em Nuvem", "Sistema de PABX em nuvem com recursos avançados", "Telefonia", None),
            ("Ura Reversa", "Unidade de Resposta Audível Reversa para campanhas", "Automação", None),
            ("Discador Preditivo", "Discador automático com inteligência preditiva", "Automação", None),
            ("Chatbot", "Chatbot para atendimento automatizado e qualificação", "Automação", None),
            ("Tronco SIP", "Serviço de tronco SIP para chamadas de voz", "Telefonia", None),
            ("0800 Virtual", "Número 0800 virtual para atendimento ao cliente", "Telefonia", None),
            ("Telefonia Móvel", "Serviços de telefonia móvel corporativa", "Telefonia", None),
        ]
        
        for name, description, category, price in default_products:
            product = Product(
                name=name,
                description=description,
                category=category,
                price=price
            )
            db.session.add(product)
        
        db.session.commit()
        print(f"Created {len(default_products)} default products.")

def populate_proposal_templates():
    """Create default proposal templates."""
    with app.app_context():
        # Check if templates already exist
        if ProposalTemplate.query.first():
            print("Proposal templates already exist in database.")
            return
        
        # Get admin user
        from src.models.user import User
        admin_user = User.query.filter_by(email='admin@jttelcom.com').first()
        if not admin_user:
            print("Admin user not found. Skipping proposal templates creation.")
            return
        
        # Template básico para PABX em Nuvem
        pabx_template = ProposalTemplate(
            name="Proposta PABX em Nuvem",
            description="Template padrão para propostas de PABX em Nuvem",
            category="Telefonia",
            subject="Proposta Comercial {proposal_number} - PABX em Nuvem para {company_name}",
            content="""
            <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #4169E1;">JT TELECOM</h1>
                    <h2>Proposta Comercial</h2>
                    <p><strong>Número:</strong> {proposal_number}</p>
                    <p><strong>Data:</strong> {current_date}</p>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Dados do Cliente</h3>
                    <p><strong>Empresa:</strong> {company_name}</p>
                    <p><strong>Contato:</strong> {name}</p>
                    <p><strong>CNPJ:</strong> {cnpj_cpf}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Telefone:</strong> {phone}</p>
                    <p><strong>Endereço:</strong> {address_street}, {address_number} - {address_neighborhood}</p>
                    <p><strong>Cidade:</strong> {address_city}/{address_state} - CEP: {address_zipcode}</p>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Solução Proposta</h3>
                    <h4>PABX em Nuvem JT Telecom</h4>
                    <p>Nossa solução de PABX em Nuvem oferece:</p>
                    <ul>
                        <li>✓ Ramais ilimitados</li>
                        <li>✓ Gravação de chamadas</li>
                        <li>✓ URA personalizada</li>
                        <li>✓ Relatórios detalhados</li>
                        <li>✓ Integração com CRM</li>
                        <li>✓ Suporte 24/7</li>
                    </ul>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Investimento</h3>
                    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                        <p style="font-size: 18px; margin: 0;"><strong>Valor Total: {total_value}</strong></p>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Condições Comerciais</h3>
                    <p><strong>Validade da Proposta:</strong> {validity_days} dias</p>
                    <p><strong>Forma de Pagamento:</strong> A combinar</p>
                    <p><strong>Prazo de Implementação:</strong> 5 dias úteis</p>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Próximos Passos</h3>
                    <p>Para dar continuidade ao projeto, precisamos:</p>
                    <ol>
                        <li>Aprovação desta proposta</li>
                        <li>Assinatura do contrato</li>
                        <li>Agendamento da implementação</li>
                    </ol>
                </div>
            </div>
            """,
            footer_text="""
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc;">
                <p><strong>JT TELECOM</strong></p>
                <p>Soluções em Telecomunicações</p>
                <p>Email: contato@jttelcom.com | Telefone: (11) 3000-0000</p>
                <p>www.jttelcom.com</p>
            </div>
            """,
            is_active=True,
            is_default=True,
            created_by=admin_user.id
        )
        
        # Template para múltiplos produtos
        multi_template = ProposalTemplate(
            name="Proposta Completa - Múltiplos Produtos",
            description="Template para propostas com vários produtos/serviços",
            category="Geral",
            subject="Proposta Comercial {proposal_number} - Soluções Completas para {company_name}",
            content="""
            <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #4169E1;">JT TELECOM</h1>
                    <h2>Proposta Comercial Completa</h2>
                    <p><strong>Número:</strong> {proposal_number}</p>
                    <p><strong>Data:</strong> {current_date}</p>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Dados do Cliente</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;"><strong>Empresa:</strong></td>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;">{company_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;"><strong>Contato:</strong></td>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;"><strong>CNPJ:</strong></td>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;">{cnpj_cpf}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;">{email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;"><strong>Telefone:</strong></td>
                            <td style="padding: 5px; border-bottom: 1px solid #eee;">{phone}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Soluções Propostas</h3>
                    <p>Apresentamos nossa suíte completa de soluções em telecomunicações:</p>
                    
                    <div style="margin: 20px 0;">
                        <h4 style="color: #4169E1;">📞 PABX em Nuvem</h4>
                        <p>Sistema completo de telefonia empresarial na nuvem.</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h4 style="color: #4169E1;">🔄 URA Reversa</h4>
                        <p>Unidade de Resposta Audível para campanhas automatizadas.</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h4 style="color: #4169E1;">🎯 Discador Preditivo</h4>
                        <p>Discador automático com inteligência artificial.</p>
                    </div>
                    
                    <div style="margin: 20px 0;">
                        <h4 style="color: #4169E1;">🤖 Chatbot</h4>
                        <p>Atendimento automatizado 24/7 para seus clientes.</p>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Investimento</h3>
                    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 5px; border-left: 4px solid #4169E1;">
                        <p style="font-size: 20px; margin: 0; text-align: center;"><strong>Valor Total: {total_value}</strong></p>
                    </div>
                </div>
                
                <div style="margin-bottom: 30px;">
                    <h3>Benefícios da Parceria</h3>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="margin: 10px 0;">✅ Redução de custos operacionais</li>
                        <li style="margin: 10px 0;">✅ Aumento da produtividade</li>
                        <li style="margin: 10px 0;">✅ Melhoria no atendimento ao cliente</li>
                        <li style="margin: 10px 0;">✅ Suporte técnico especializado</li>
                        <li style="margin: 10px 0;">✅ Implementação rápida e segura</li>
                    </ul>
                </div>
            </div>
            """,
            footer_text="""
            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #4169E1;">
                <p style="color: #4169E1; font-size: 18px; margin: 0;"><strong>JT TELECOM</strong></p>
                <p style="margin: 5px 0;">Transformando comunicação em resultados</p>
                <p style="margin: 5px 0;">📧 contato@jttelcom.com | 📞 (11) 3000-0000</p>
                <p style="margin: 5px 0;">🌐 www.jttelcom.com</p>
            </div>
            """,
            is_active=True,
            is_default=False,
            created_by=admin_user.id
        )
        
        # Template simples
        simple_template = ProposalTemplate(
            name="Proposta Simples",
            description="Template básico para propostas rápidas",
            category="Geral",
            subject="Proposta {proposal_number} - {company_name}",
            content="""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4169E1; text-align: center;">Proposta Comercial</h2>
                <p style="text-align: center;"><strong>{proposal_number}</strong> | {current_date}</p>
                
                <hr style="margin: 30px 0;">
                
                <h3>Cliente</h3>
                <p><strong>{company_name}</strong><br>
                Contato: {name}<br>
                Email: {email}<br>
                Telefone: {phone}</p>
                
                <h3>Proposta</h3>
                <p>Prezado(a) {name},</p>
                <p>Conforme nossa conversa, apresentamos nossa proposta para atendimento das necessidades de telecomunicações da {company_name}.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px;">
                    <h4 style="margin-top: 0;">Valor da Proposta</h4>
                    <p style="font-size: 18px; margin: 0;"><strong>{total_value}</strong></p>
                </div>
                
                <p><strong>Validade:</strong> {validity_days} dias</p>
                
                <p>Aguardamos seu retorno para darmos continuidade ao projeto.</p>
                
                <p>Atenciosamente,<br>
                Equipe JT Telecom</p>
            </div>
            """,
            footer_text="",
            is_active=True,
            is_default=False,
            created_by=admin_user.id
        )
        
        db.session.add(pabx_template)
        db.session.add(multi_template)
        db.session.add(simple_template)
        db.session.commit()
        
        print("Created 3 default proposal templates.")

def populate_contract_templates():
    """Cria templates de contratos padrão."""
    print("Criando templates de contratos...")
    
    templates = [
        {
            'name': 'Contrato de Prestação de Serviços - PABX em Nuvem',
            'description': 'Template padrão para contratos de PABX em Nuvem',
            'category': 'Telefonia',
            'contract_type': 'Prestação de Serviços',
            'title': 'CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE TELEFONIA - {contract_number}',
            'content': '''
            <h2>CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE TELEFONIA</h2>
            
            <p><strong>CONTRATANTE:</strong> {company_name}, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº {cnpj_cpf}, com sede na {address_street}, {address_number}, {address_neighborhood}, {address_city}/{address_state}, CEP {address_zipcode}, neste ato representada por {name}.</p>
            
            <p><strong>CONTRATADA:</strong> JT TELECOM LTDA, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº 12.345.678/0001-90, com sede na Rua das Telecomunicações, 123, Centro, São Paulo/SP, CEP 01234-567.</p>
            
            <h3>CLÁUSULA 1ª - DO OBJETO</h3>
            <p>O presente contrato tem por objeto a prestação de serviços de telefonia em nuvem (PABX Virtual), incluindo:</p>
            <ul>
                <li>Fornecimento de sistema PABX em nuvem</li>
                <li>Configuração e implementação do sistema</li>
                <li>Suporte técnico especializado</li>
                <li>Manutenção e atualizações do sistema</li>
            </ul>
            
            <h3>CLÁUSULA 2ª - DO VALOR E FORMA DE PAGAMENTO</h3>
            <p>O valor total do contrato é de {contract_value}, a ser pago mensalmente no valor de R$ {monthly_value}, com vencimento todo dia 10 de cada mês.</p>
            
            <h3>CLÁUSULA 3ª - DA VIGÊNCIA</h3>
            <p>O presente contrato terá vigência de {duration_months} meses, iniciando-se em {start_date} e encerrando-se em {end_date}.</p>
            
            <h3>CLÁUSULA 4ª - DAS RESPONSABILIDADES</h3>
            <p>A CONTRATADA se compromete a fornecer os serviços com qualidade e disponibilidade mínima de 99,5%.</p>
            <p>A CONTRATANTE se compromete a efetuar os pagamentos nas datas acordadas.</p>
            
            <h3>CLÁUSULA 5ª - DA RESCISÃO</h3>
            <p>O presente contrato poderá ser rescindido por qualquer das partes mediante aviso prévio de {cancellation_notice_days} dias.</p>
            
            <h3>CLÁUSULA 6ª - DO FORO</h3>
            <p>Fica eleito o foro da Comarca de São Paulo/SP para dirimir quaisquer questões oriundas do presente contrato.</p>
            
            <p>E por estarem assim justos e contratados, firmam o presente instrumento em duas vias de igual teor.</p>
            
            <p>{address_city}, {current_date}</p>
            ''',
            'footer_text': '''
            <p style="text-align: center; margin-top: 30px;">
                <strong>JT TELECOM LTDA</strong><br>
                CNPJ: 12.345.678/0001-90<br>
                Telefone: (11) 3000-0000<br>
                Email: contratos@jttelcom.com
            </p>
            ''',
            'default_duration_months': 12,
            'auto_renewal': True,
            'cancellation_notice_days': 30,
            'requires_witness': False
        },
        {
            'name': 'Contrato de Licenciamento de Software',
            'description': 'Template para contratos de licenciamento de software',
            'category': 'Software',
            'contract_type': 'Licenciamento',
            'title': 'CONTRATO DE LICENCIAMENTO DE SOFTWARE - {contract_number}',
            'content': '''
            <h2>CONTRATO DE LICENCIAMENTO DE SOFTWARE</h2>
            
            <p><strong>LICENCIANTE:</strong> JT TELECOM LTDA, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº 12.345.678/0001-90.</p>
            
            <p><strong>LICENCIADO:</strong> {company_name}, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº {cnpj_cpf}, representada por {name}.</p>
            
            <h3>CLÁUSULA 1ª - DO OBJETO</h3>
            <p>O presente contrato tem por objeto o licenciamento de uso do software de telefonia desenvolvido pela LICENCIANTE.</p>
            
            <h3>CLÁUSULA 2ª - DA LICENÇA</h3>
            <p>A licença concedida é não exclusiva, intransferível e limitada ao uso interno da LICENCIADA.</p>
            
            <h3>CLÁUSULA 3ª - DO VALOR</h3>
            <p>O valor da licença é de {contract_value}, a ser pago conforme condições acordadas.</p>
            
            <h3>CLÁUSULA 4ª - DA VIGÊNCIA</h3>
            <p>A licença terá vigência de {duration_months} meses, de {start_date} a {end_date}.</p>
            
            <h3>CLÁUSULA 5ª - DAS LIMITAÇÕES</h3>
            <p>É vedado ao LICENCIADO reproduzir, modificar ou distribuir o software sem autorização expressa.</p>
            
            <p>{address_city}, {current_date}</p>
            ''',
            'footer_text': '''
            <p style="text-align: center;">
                <strong>JT TELECOM LTDA</strong><br>
                Departamento Jurídico<br>
                juridico@jttelcom.com
            </p>
            ''',
            'default_duration_months': 24,
            'auto_renewal': False,
            'cancellation_notice_days': 60,
            'requires_witness': True
        },
        {
            'name': 'Contrato de Consultoria Técnica',
            'description': 'Template para contratos de consultoria técnica',
            'category': 'Consultoria',
            'contract_type': 'Prestação de Serviços',
            'title': 'CONTRATO DE CONSULTORIA TÉCNICA - {contract_number}',
            'content': '''
            <h2>CONTRATO DE CONSULTORIA TÉCNICA</h2>
            
            <p><strong>CONTRATANTE:</strong> {company_name}, CNPJ {cnpj_cpf}, representada por {name}.</p>
            
            <p><strong>CONTRATADA:</strong> JT TELECOM LTDA, CNPJ 12.345.678/0001-90.</p>
            
            <h3>OBJETO</h3>
            <p>Prestação de serviços de consultoria técnica especializada em telecomunicações.</p>
            
            <h3>ESCOPO DOS SERVIÇOS</h3>
            <ul>
                <li>Análise da infraestrutura atual</li>
                <li>Elaboração de projeto técnico</li>
                <li>Acompanhamento da implementação</li>
                <li>Treinamento da equipe técnica</li>
            </ul>
            
            <h3>VALOR E PAGAMENTO</h3>
            <p>Valor total: {contract_value}</p>
            <p>Forma de pagamento: Conforme cronograma anexo</p>
            
            <h3>PRAZO</h3>
            <p>Prazo de execução: {duration_months} meses</p>
            <p>Início: {start_date}</p>
            <p>Término: {end_date}</p>
            
            <p>{address_city}, {current_date}</p>
            ''',
            'footer_text': '''
            <p style="text-align: center;">
                <em>Contrato de Consultoria Técnica - JT Telecom</em>
            </p>
            ''',
            'default_duration_months': 6,
            'auto_renewal': False,
            'cancellation_notice_days': 15,
            'requires_witness': False
        }
    ]
    
    for template_data in templates:
        existing = ContractTemplate.query.filter_by(name=template_data['name']).first()
        if not existing:
            template = ContractTemplate(**template_data, created_by='admin')
            db.session.add(template)
            print(f"Template criado: {template_data['name']}")
        else:
            print(f"Template já existe: {template_data['name']}")
    
    db.session.commit()
    print("Templates de contratos criados com sucesso!")

def populate_chatbot_data():
    """Cria dados padrão do chatbot."""
    print("Criando dados padrão do chatbot...")
    
    # Configuração de IA padrão
    ai_config = ChatAIConfig.query.filter_by(is_default=True).first()
    if not ai_config:
        ai_config = ChatAIConfig(
            name='Configuração Padrão OpenAI',
            api_key='sk-your-openai-api-key-here',  # Deve ser configurado pelo usuário
            model='gpt-4o',
            max_tokens=1000,
            temperature=0.7,
            system_prompt='''Você é um assistente virtual da JT Telecom, especializada em soluções de telefonia em nuvem.

Sua personalidade:
- Profissional, mas amigável e acessível
- Especialista em telecomunicações
- Focado em ajudar o cliente a encontrar a melhor solução
- Sempre educado e paciente

Seus produtos principais:
- PABX em Nuvem: Sistema de telefonia completo na nuvem
- URA Reversa: Sistema de atendimento automático inteligente
- Discador Preditivo: Ferramenta para otimizar campanhas de vendas
- Chatbot: Atendimento automatizado via WhatsApp
- Tronco SIP: Conectividade telefônica digital
- 0800 Virtual: Números gratuitos para seus clientes
- Telefonia Móvel: Soluções móveis corporativas

Diretrizes:
1. Sempre seja útil e tente resolver a dúvida do cliente
2. Se não souber algo específico, seja honesto e ofereça transferir para um especialista
3. Colete informações básicas: nome, empresa, telefone, necessidade
4. Mantenha as respostas concisas mas completas
5. Use linguagem brasileira informal mas profissional
6. Sempre termine oferecendo ajuda adicional

Se o cliente mencionar palavras como "falar com humano", "atendente", "pessoa", "não entendi", transfira imediatamente para atendimento humano.''',
            context_window=10,
            fallback_enabled=True,
            auto_handoff=True,
            handoff_keywords=['humano', 'atendente', 'pessoa', 'não entendi', 'falar com alguém'],
            typing_delay=2,
            max_response_time=30,
            is_active=True,
            is_default=True,
            created_by='admin'
        )
        db.session.add(ai_config)
        print("Configuração de IA padrão criada")
    
    # Fluxo de boas-vindas
    welcome_flow = ChatFlow.query.filter_by(name='Fluxo de Boas-vindas').first()
    if not welcome_flow:
        welcome_flow_data = {
            "steps": {
                "start": {
                    "type": "text",
                    "message": "👋 Olá! Bem-vindo à JT Telecom!\n\nSou seu assistente virtual e estou aqui para ajudar você com nossas soluções de telefonia em nuvem.\n\nPara começar, qual é o seu nome?",
                    "next_step": "collect_name"
                },
                "collect_name": {
                    "type": "input",
                    "variable_name": "customer_name",
                    "validation": {
                        "type": "required"
                    },
                    "next_step": "collect_company"
                },
                "collect_company": {
                    "type": "text",
                    "message": "Prazer em conhecê-lo, {customer_name}! 😊\n\nQual é o nome da sua empresa?",
                    "next_step": "collect_company_input"
                },
                "collect_company_input": {
                    "type": "input",
                    "variable_name": "company_name",
                    "validation": {
                        "type": "required"
                    },
                    "next_step": "collect_phone"
                },
                "collect_phone": {
                    "type": "text",
                    "message": "Perfeito! E qual é o melhor telefone para contato?",
                    "next_step": "collect_phone_input"
                },
                "collect_phone_input": {
                    "type": "input",
                    "variable_name": "phone",
                    "validation": {
                        "type": "phone"
                    },
                    "next_step": "show_services"
                },
                "show_services": {
                    "type": "buttons",
                    "message": "Ótimo, {customer_name}! Agora me conte, qual solução da JT Telecom mais te interessa?",
                    "variable_name": "interest",
                    "buttons": [
                        {
                            "id": "pabx",
                            "title": "📞 PABX em Nuvem",
                            "value": "PABX em Nuvem",
                            "next_step": "pabx_info"
                        },
                        {
                            "id": "ura",
                            "title": "🤖 URA Reversa",
                            "value": "URA Reversa",
                            "next_step": "ura_info"
                        },
                        {
                            "id": "discador",
                            "title": "📊 Discador Preditivo",
                            "value": "Discador Preditivo",
                            "next_step": "discador_info"
                        },
                        {
                            "id": "outros",
                            "title": "🔍 Outras soluções",
                            "value": "Outras soluções",
                            "next_step": "other_services"
                        }
                    ]
                },
                "pabx_info": {
                    "type": "text",
                    "message": "📞 *PABX em Nuvem da JT Telecom*\n\n✅ Sistema completo de telefonia\n✅ Sem investimento em equipamentos\n✅ Ramais ilimitados\n✅ Integração com CRM\n✅ Relatórios detalhados\n✅ Suporte 24/7\n\nGostaria de agendar uma demonstração gratuita?",
                    "next_step": "schedule_demo"
                },
                "ura_info": {
                    "type": "text",
                    "message": "🤖 *URA Reversa da JT Telecom*\n\n✅ Atendimento automático inteligente\n✅ Reduz tempo de espera\n✅ Melhora experiência do cliente\n✅ Integração com sistemas\n✅ Relatórios de performance\n\nQuer saber mais detalhes?",
                    "next_step": "schedule_demo"
                },
                "discador_info": {
                    "type": "text",
                    "message": "📊 *Discador Preditivo da JT Telecom*\n\n✅ Otimiza campanhas de vendas\n✅ Aumenta produtividade em até 300%\n✅ Relatórios em tempo real\n✅ Integração com CRM\n✅ Compliance com LGPD\n\nVamos agendar uma apresentação?",
                    "next_step": "schedule_demo"
                },
                "other_services": {
                    "type": "text",
                    "message": "🔍 *Outras soluções JT Telecom:*\n\n📱 Chatbot WhatsApp\n📞 Tronco SIP\n🆓 0800 Virtual\n📱 Telefonia Móvel\n\nQual dessas soluções te interessa mais? Ou prefere falar com um especialista?",
                    "next_step": "ai_or_human"
                },
                "schedule_demo": {
                    "type": "buttons",
                    "message": "Como prefere prosseguir?",
                    "buttons": [
                        {
                            "id": "demo",
                            "title": "📅 Agendar demonstração",
                            "value": "Agendar demonstração",
                            "next_step": "transfer_to_human"
                        },
                        {
                            "id": "info",
                            "title": "📋 Receber informações",
                            "value": "Receber informações",
                            "next_step": "collect_email"
                        },
                        {
                            "id": "human",
                            "title": "👤 Falar com especialista",
                            "value": "Falar com especialista",
                            "next_step": "transfer_to_human"
                        }
                    ]
                },
                "collect_email": {
                    "type": "text",
                    "message": "📧 Para enviar as informações, qual é o seu e-mail?",
                    "next_step": "collect_email_input"
                },
                "collect_email_input": {
                    "type": "input",
                    "variable_name": "email",
                    "validation": {
                        "type": "email"
                    },
                    "next_step": "create_lead"
                },
                "create_lead": {
                    "type": "webhook",
                    "webhook_url": "/api/leads",
                    "method": "POST",
                    "next_step": "thank_you"
                },
                "thank_you": {
                    "type": "text",
                    "message": "🎉 Perfeito, {customer_name}!\n\nSuas informações foram registradas e em breve você receberá nosso material.\n\nSe precisar de mais alguma coisa, é só chamar!\n\n*JT Telecom - Conectando seu sucesso!* 🚀",
                    "next_step": "end"
                },
                "transfer_to_human": {
                    "type": "text",
                    "message": "👤 Perfeito! Vou transferir você para um de nossos especialistas.\n\nEm instantes alguém da nossa equipe entrará em contato.\n\nObrigado por escolher a JT Telecom! 😊",
                    "next_step": "end"
                },
                "ai_or_human": {
                    "type": "ai",
                    "context": "O cliente está interessado em outras soluções da JT Telecom. Seja útil e tente identificar a necessidade específica.",
                    "next_step": "end"
                },
                "end": {
                    "type": "text",
                    "message": "Conversa finalizada. Digite qualquer coisa para reiniciar.",
                    "next_step": "start"
                }
            }
        }
        
        welcome_flow = ChatFlow(
            name='Fluxo de Boas-vindas',
            description='Fluxo padrão de boas-vindas e qualificação de leads',
            trigger_keywords=['oi', 'olá', 'hello', 'hi', 'bom dia', 'boa tarde', 'boa noite'],
            is_default=True,
            is_active=True,
            priority=1,
            flow_data=welcome_flow_data,
            ai_enabled=True,
            ai_fallback=True,
            ai_context='Fluxo de qualificação inicial para produtos JT Telecom',
            created_by='admin'
        )
        db.session.add(welcome_flow)
        print("Fluxo de boas-vindas criado")
    
    # Fluxo de suporte técnico
    support_flow = ChatFlow.query.filter_by(name='Suporte Técnico').first()
    if not support_flow:
        support_flow_data = {
            "steps": {
                "start": {
                    "type": "text",
                    "message": "🔧 *Suporte Técnico JT Telecom*\n\nOlá! Estou aqui para ajudar com questões técnicas.\n\nQual tipo de problema você está enfrentando?",
                    "next_step": "problem_type"
                },
                "problem_type": {
                    "type": "buttons",
                    "message": "Selecione o tipo de problema:",
                    "variable_name": "problem_type",
                    "buttons": [
                        {
                            "id": "connection",
                            "title": "🌐 Problemas de conexão",
                            "value": "Problemas de conexão",
                            "next_step": "connection_help"
                        },
                        {
                            "id": "audio",
                            "title": "🔊 Problemas de áudio",
                            "value": "Problemas de áudio",
                            "next_step": "audio_help"
                        },
                        {
                            "id": "config",
                            "title": "⚙️ Configurações",
                            "value": "Configurações",
                            "next_step": "config_help"
                        },
                        {
                            "id": "other",
                            "title": "❓ Outro problema",
                            "value": "Outro problema",
                            "next_step": "describe_problem"
                        }
                    ]
                },
                "connection_help": {
                    "type": "text",
                    "message": "🌐 *Problemas de Conexão - Verificações Básicas:*\n\n1️⃣ Verifique sua conexão com a internet\n2️⃣ Teste a velocidade da internet (mín. 1Mbps por ramal)\n3️⃣ Verifique se o firewall não está bloqueando\n4️⃣ Reinicie seu roteador\n\nO problema foi resolvido?",
                    "next_step": "problem_resolved"
                },
                "audio_help": {
                    "type": "text",
                    "message": "🔊 *Problemas de Áudio - Verificações:*\n\n1️⃣ Verifique o volume do dispositivo\n2️⃣ Teste com outro headset/telefone\n3️⃣ Verifique as configurações de áudio\n4️⃣ Reinicie o aplicativo/softphone\n\nO problema foi resolvido?",
                    "next_step": "problem_resolved"
                },
                "config_help": {
                    "type": "text",
                    "message": "⚙️ *Configurações - Precisa de ajuda com:*\n\n• Configuração de ramal\n• Configuração de softphone\n• Configuração de redirecionamento\n• Outras configurações\n\nPara configurações específicas, vou transferir você para nosso suporte especializado.",
                    "next_step": "transfer_to_support"
                },
                "describe_problem": {
                    "type": "text",
                    "message": "❓ Por favor, descreva detalhadamente o problema que você está enfrentando:",
                    "next_step": "collect_problem_description"
                },
                "collect_problem_description": {
                    "type": "input",
                    "variable_name": "problem_description",
                    "validation": {
                        "type": "required"
                    },
                    "next_step": "transfer_to_support"
                },
                "problem_resolved": {
                    "type": "buttons",
                    "message": "O problema foi resolvido?",
                    "buttons": [
                        {
                            "id": "yes",
                            "title": "✅ Sim, resolvido",
                            "value": "Sim",
                            "next_step": "thank_you"
                        },
                        {
                            "id": "no",
                            "title": "❌ Não, ainda persiste",
                            "value": "Não",
                            "next_step": "transfer_to_support"
                        }
                    ]
                },
                "transfer_to_support": {
                    "type": "text",
                    "message": "🔧 Vou transferir você para nosso suporte técnico especializado.\n\nEm instantes um técnico entrará em contato para resolver seu problema.\n\n*Horário de atendimento: 8h às 18h, de segunda a sexta.*",
                    "next_step": "end"
                },
                "thank_you": {
                    "type": "text",
                    "message": "🎉 Ótimo! Fico feliz em ter ajudado!\n\nSe precisar de mais alguma coisa, é só chamar.\n\n*JT Telecom - Suporte que funciona!* 🚀",
                    "next_step": "end"
                },
                "end": {
                    "type": "text",
                    "message": "Atendimento finalizado. Digite 'suporte' para iniciar novo atendimento.",
                    "next_step": "start"
                }
            }
        }
        
        support_flow = ChatFlow(
            name='Suporte Técnico',
            description='Fluxo para atendimento de suporte técnico',
            trigger_keywords=['suporte', 'problema', 'ajuda', 'não funciona', 'erro'],
            is_default=False,
            is_active=True,
            priority=2,
            flow_data=support_flow_data,
            ai_enabled=True,
            ai_fallback=True,
            ai_context='Suporte técnico para produtos JT Telecom. Seja útil e tente resolver problemas básicos.',
            created_by='admin'
        )
        db.session.add(support_flow)
        print("Fluxo de suporte técnico criado")
    
    db.session.commit()
    print("Dados padrão do chatbot criados com sucesso!")

def populate_telephony_data():
    """Create sample telephony call data."""
    with app.app_context():
        # Check if data already exists
        if TelephonyCall.query.first():
            print("Telephony call data already exists in database.")
            return

        from src.models.user import User
        from src.models.lead import Lead
        from datetime import datetime, timedelta
        import random

        admin_user = User.query.filter_by(email=\'admin@jttelcom.com\').first()
        if not admin_user:
            print("Admin user not found. Skipping telephony data creation.")
            return

        leads = Lead.query.all()
        if not leads:
            print("No leads found. Skipping telephony data creation.")
            return

        call_types = [\'inbound\', \'outbound\']
        call_statuses = [\'completed\', \'missed\', \'failed\']

        telephony_calls = []
        for _ in range(20):
            lead = random.choice(leads)
            call_type = random.choice(call_types)
            call_status = random.choice(call_statuses)
            duration = random.randint(30, 600) if call_status == \'completed\' else 0
            call_time = datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23), minutes=random.randint(1, 59))

            call = TelephonyCall(
                lead_id=lead.id,
                user_id=admin_user.id,
                call_type=call_type,
                call_status=call_status,
                duration=duration,
                call_time=call_time,
                phone_number=lead.phone,
                recording_url=f\'http://recordings.jttelcom.com/{lead.id}-{call_time.strftime(\"%Y%m%d%H%M%S\")}.mp3\' if call_status == \'completed\' else None
            )
            telephony_calls.append(call)
            db.session.add(call)

        db.session.commit()
        print(f"Created {len(telephony_calls)} sample telephony calls.")


if __name__ == \'__main__\':
    with app.app_context():
        db.create_all()
    populate_tags()
    populate_field_templates()
    populate_products()
    populate_proposal_templates()
    populate_contract_templates()
    populate_chatbot_data()
    populate_telephony_data()