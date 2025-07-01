import os
import re

# Lista de arquivos de rotas para corrigir
route_files = [
    'routes/auth.py',
    'routes/automation.py', 
    'routes/chatbot.py',
    'routes/clients.py',
    'routes/contracts.py',
    'routes/dashboard.py',
    'routes/leads.py',
    'routes/pipelines.py',
    'routes/proposals.py',
    'routes/tasks.py',
    'routes/telephony.py',
    'routes/tenant_admin.py',
    'routes/user.py'
]

for file_path in route_files:
    if os.path.exists(file_path):
        print(f"Corrigindo {file_path}...")
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Verificar se já tem a importação correta
        if 'from flask import Blueprint' not in content:
            # Adicionar importação no início
            lines = content.split('\n')
            
            # Encontrar onde inserir a importação
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('from ') or line.strip().startswith('import '):
                    insert_index = i
                    break
            
            # Inserir a importação
            lines.insert(insert_index, 'from flask import Blueprint, request, jsonify')
            
            # Remover linhas duplicadas
            seen = set()
            new_lines = []
            for line in lines:
                if line not in seen or not line.strip().startswith('from flask import'):
                    new_lines.append(line)
                    seen.add(line)
            
            # Escrever arquivo corrigido
            with open(file_path, 'w') as f:
                f.write('\n'.join(new_lines))
            
            print(f"✅ {file_path} corrigido")
        else:
            print(f"⚠️ {file_path} já tem importação correta")

print("🎉 Todas as correções concluídas!")
