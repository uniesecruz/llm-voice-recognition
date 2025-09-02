"""
Script para baixar o modelo Llama quantizado do Hugging Face
"""
import os
import requests
from pathlib import Path

def download_model():
    """Baixa o modelo Llama quantizado do Hugging Face"""
    
    # URL do modelo no Hugging Face (modelo menor e compatível)
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    
    # Caminho onde salvar o modelo
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "llama-2-7b-chat.Q4_K_M.gguf"
    
    # Verifica se o modelo já existe
    if model_path.exists():
        print(f"Modelo já existe em: {model_path}")
        return str(model_path)
    
    print("Iniciando download do modelo Llama-2-7B-Chat quantizado...")
    print("Isso pode demorar alguns minutos dependendo da sua conexão...")
    
    try:
        # Faz o download com barra de progresso
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Mostra progresso
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\rProgresso: {progress:.1f}%", end="", flush=True)
        
        print(f"\nModelo baixado com sucesso em: {model_path}")
        return str(model_path)
        
    except Exception as e:
        print(f"Erro ao baixar o modelo: {e}")
        if model_path.exists():
            model_path.unlink()  # Remove arquivo parcialmente baixado
        return None

if __name__ == "__main__":
    download_model()
