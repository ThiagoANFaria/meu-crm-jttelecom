import sys
import os

# Adiciona o diretório src ao path do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

print(f"Diretório atual: {current_dir}")
print(f"Caminho src: {src_path}")
print(f"Arquivos no diretório atual: {os.listdir(current_dir)}")
print(f"Arquivos no src: {os.listdir(src_path) if os.path.exists(src_path) else 'Pasta src não existe'}")

try:
    # Importa a função create_app da pasta src (corrigindo o conflito de nomes)
    from src.main import create_app
    print("✅ Importação bem-sucedida!")
    
    # Cria a instância da aplicação Flask para o Gunicorn
    app = create_app()
    
    if __name__ == "__main__":
        print("🚀 Iniciando aplicação Flask...")
        app.run(host="0.0.0.0", port=5000, debug=False)
        
except ImportError as e:
    print(f"❌ Erro na importação: {e}")
    print("Verifique se o arquivo src/main.py existe e está correto")
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()

