import os
import re

# Lista de arquivos que usam flasgger
files_with_flasgger = [
    'routes/automation.py',
    'routes/chatbot.py', 
    'routes/contracts.py',
    'routes/telephony.py',
    'routes/user.py'
]

flasgger_import_fix = '''# Importação opcional de flasgger
try:
    from flasgger import swag_from
except ImportError:
    # Fallback se flasgger não estiver disponível
    def swag_from(spec):
        def decorator(func):
            return func
        return decorator'''

for file_path in files_with_flasgger:
    if os.path.exists(file_path):
        print(f"Corrigindo {file_path}...")
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Substituir importação simples de flasgger
        if 'from flasgger import swag_from' in content:
            content = content.replace(
                'from flasgger import swag_from',
                flasgger_import_fix
            )
            
            # Escrever arquivo corrigido
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"✅ {file_path} corrigido")
        else:
            print(f"⚠️ {file_path} não precisa de correção")

print("🎉 Todas as correções de flasgger concluídas!")
