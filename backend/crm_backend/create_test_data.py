#!/usr/bin/env python3
"""
Script para criar dados de teste para o dashboard
"""
import os
import sys
from datetime import datetime, date, timedelta
import random

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.lead import Lead
from src.models.pipeline import Pipeline, PipelineStage, Product, Opportunity
from flask import Flask

# Configure Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crm_user:crm_password@localhost/crm_jttelcom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_test_data():
    """Create test data for dashboard."""
    with app.app_context():
        print("Creating test data for dashboard...")
        
        # Get admin user
        admin_user = User.query.filter_by(email='admin@jttelcom.com').first()
        if not admin_user:
            print("Admin user not found. Please create admin user first.")
            return
        
        # Get pipelines
        prospection_pipeline = Pipeline.query.filter_by(pipeline_type='prospection').first()
        sales_pipeline = Pipeline.query.filter_by(pipeline_type='sales').first()
        
        if not prospection_pipeline or not sales_pipeline:
            print("Pipelines not found. Please create pipelines first.")
            return
        
        # Get products
        products = Product.query.all()
        if not products:
            print("No products found. Please create products first.")
            return
        
        # Create test leads
        lead_names = [
            ("João Silva", "Tech Solutions Ltda", "joao@techsolutions.com", "(11) 99999-1111"),
            ("Maria Santos", "Inovação Digital", "maria@inovacao.com", "(11) 99999-2222"),
            ("Pedro Costa", "Empresa ABC", "pedro@abc.com", "(11) 99999-3333"),
            ("Ana Oliveira", "StartupXYZ", "ana@startupxyz.com", "(11) 99999-4444"),
            ("Carlos Ferreira", "Corporação Beta", "carlos@beta.com", "(11) 99999-5555"),
            ("Lucia Rodrigues", "Negócios Online", "lucia@online.com", "(11) 99999-6666"),
            ("Roberto Lima", "Soluções Tech", "roberto@solucoes.com", "(11) 99999-7777"),
            ("Fernanda Alves", "Digital Corp", "fernanda@digital.com", "(11) 99999-8888"),
        ]
        
        sources = ["Website", "Indicação", "Google Ads", "LinkedIn", "Telefone", "Email Marketing"]
        statuses = ["Novo", "Qualificado", "Em Contato", "Interessado", "Desqualificado"]
        
        created_leads = []
        for i, (name, company, email, phone) in enumerate(lead_names):
            # Create lead with random data from past 60 days
            created_date = datetime.now() - timedelta(days=random.randint(1, 60))
            
            lead = Lead(
                name=name,
                company_name=company,
                email=email,
                phone=phone,
                whatsapp=phone,
                origin=random.choice(sources),
                status=random.choice(statuses),
                score=random.randint(20, 100),
                assigned_to=admin_user.id,
                created_at=created_date,
                updated_at=created_date
            )
            db.session.add(lead)
            created_leads.append(lead)
        
        db.session.flush()  # Get lead IDs
        
        # Create opportunities
        opportunity_titles = [
            "Implementação PABX em Nuvem - Tech Solutions",
            "Projeto URA Reversa - Inovação Digital", 
            "Sistema Completo - Empresa ABC",
            "Chatbot + Discador - StartupXYZ",
            "Tronco SIP Enterprise - Corporação Beta",
            "0800 Virtual - Negócios Online",
            "Telefonia Móvel Corporativa - Soluções Tech",
            "Projeto Completo - Digital Corp"
        ]
        
        priorities = ["low", "medium", "high"]
        
        for i, lead in enumerate(created_leads[:6]):  # Create opportunities for first 6 leads
            # Random pipeline
            pipeline = random.choice([prospection_pipeline, sales_pipeline])
            
            # Random stage (not final stages)
            active_stages = [s for s in pipeline.stages if not s.is_final]
            stage = random.choice(active_stages)
            
            # Random value
            value = random.choice([1500, 2500, 5000, 8000, 12000, 15000, 25000])
            
            # Random close date (future)
            expected_close = date.today() + timedelta(days=random.randint(15, 90))
            
            # Create opportunity
            opportunity = Opportunity(
                title=opportunity_titles[i],
                description=f"Oportunidade de venda para {lead.company_name}",
                lead_id=lead.id,
                pipeline_id=pipeline.id,
                stage_id=stage.id,
                assigned_to=admin_user.id,
                value=value,
                probability=random.randint(30, 90),
                expected_close_date=expected_close,
                priority=random.choice(priorities),
                source=lead.origin,
                created_at=lead.created_at + timedelta(days=random.randint(1, 5))
            )
            db.session.add(opportunity)
            db.session.flush()
            
            # Add random products to opportunity
            selected_products = random.sample(products, random.randint(1, 3))
            opportunity.products.extend(selected_products)
        
        # Create some won/lost opportunities for statistics
        won_lost_data = [
            ("Venda Fechada - Cliente A", 15000, "won", -30),
            ("Venda Fechada - Cliente B", 8000, "won", -20),
            ("Venda Fechada - Cliente C", 25000, "won", -15),
            ("Oportunidade Perdida - Cliente D", 12000, "lost", -25),
            ("Venda Fechada - Cliente E", 5000, "won", -10),
        ]
        
        for title, value, status, days_ago in won_lost_data:
            close_date = date.today() + timedelta(days=days_ago)
            created_date = close_date - timedelta(days=random.randint(10, 30))
            
            # Use first lead for simplicity
            opportunity = Opportunity(
                title=title,
                description=f"Oportunidade {status}",
                lead_id=created_leads[0].id,
                pipeline_id=sales_pipeline.id,
                stage_id=sales_pipeline.stages[-1].id if status == "won" else sales_pipeline.stages[-2].id,
                assigned_to=admin_user.id,
                value=value,
                probability=100 if status == "won" else 0,
                expected_close_date=close_date,
                actual_close_date=close_date,
                status=status,
                priority="high",
                source="Indicação",
                created_at=created_date
            )
            db.session.add(opportunity)
            db.session.flush()
            
            # Add products
            selected_products = random.sample(products, random.randint(1, 2))
            opportunity.products.extend(selected_products)
        
        db.session.commit()
        print(f"Created {len(created_leads)} test leads and multiple opportunities")
        print("Test data creation completed!")

if __name__ == '__main__':
    create_test_data()

