"""
Script de teste rápido para verificar os componentes principais
"""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🧪 Testando importações...")
    
    try:
        import speech_recognition as sr
        print("✅ speech_recognition OK")
    except ImportError as e:
        print(f"❌ speech_recognition: {e}")
        return False
    
    try:
        import whisper
        print("✅ whisper OK")
    except ImportError as e:
        print(f"❌ whisper: {e}")
        return False
    
    try:
        from langchain.llms import CTransformers
        print("✅ langchain OK")
    except ImportError as e:
        print(f"❌ langchain: {e}")
        return False
    
    try:
        from gtts import gTTS
        print("✅ gTTS OK")
    except ImportError as e:
        print(f"❌ gTTS: {e}")
        return False
    
    try:
        import pygame
        print("✅ pygame OK")
    except ImportError as e:
        print(f"❌ pygame: {e}")
        return False
    
    return True

def test_model_file():
    """Verifica se o arquivo do modelo existe"""
    print("\\n📁 Verificando arquivo do modelo...")
    
    from pathlib import Path
    models_dir = Path("models")
    
    if not models_dir.exists():
        print("❌ Pasta 'models' não encontrada")
        return False
    
    model_files = list(models_dir.glob("*.gguf"))
    if not model_files:
        print("❌ Nenhum arquivo .gguf encontrado na pasta models")
        return False
    
    model_file = model_files[0]
    file_size = model_file.stat().st_size / (1024**3)  # Tamanho em GB
    print(f"✅ Modelo encontrado: {model_file.name}")
    print(f"✅ Tamanho: {file_size:.2f} GB")
    
    return True

def test_whisper_model():
    """Testa se o modelo Whisper pode ser carregado"""
    print("\\n🎙️ Testando modelo Whisper...")
    
    try:
        import whisper
        model = whisper.load_model("base")
        print("✅ Modelo Whisper 'base' carregado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar Whisper: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🔍 TESTE RÁPIDO DO ASSISTENTE DE VOZ")
    print("=" * 50)
    
    # Teste 1: Importações
    if not test_imports():
        print("\\n❌ Falha nos testes de importação")
        print("Execute: pip install -r requirements.txt")
        return
    
    # Teste 2: Arquivo do modelo
    if not test_model_file():
        print("\\n❌ Falha no teste do modelo")
        print("Execute: python download_model.py")
        return
    
    # Teste 3: Modelo Whisper
    if not test_whisper_model():
        print("\\n❌ Falha no teste do Whisper")
        return
    
    print("\\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("✅ O assistente de voz está pronto para uso!")
    print("\\nExecute: python main.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
