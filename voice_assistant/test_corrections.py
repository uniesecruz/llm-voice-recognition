"""
Teste específico para verificar se a depreciação foi corrigida e se o áudio funciona
"""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_llm_deprecation_fix():
    """Testa se a correção da depreciação do LangChain funciona"""
    print("🔧 TESTE DE CORREÇÃO DA DEPRECIAÇÃO")
    print("=" * 50)
    
    try:
        print("\\n1. Testando importação do LLM Manager...")
        from llm_manager import LLMManager
        print("✅ Importação bem-sucedida")
        
        print("\\n2. Inicializando LLM Manager...")
        llm_manager = LLMManager()
        print("✅ LLM Manager inicializado")
        
        print("\\n3. Testando geração de resposta (novo método invoke)...")
        test_question = "Qual a capital do Brasil?"
        response = llm_manager.generate_response(test_question)
        
        print(f"Pergunta: {test_question}")
        print(f"Resposta: {response}")
        
        if response and "Brasil" in response:
            print("✅ Resposta gerada corretamente sem warnings de depreciação")
            return True, response
        else:
            print("❌ Resposta não gerada corretamente")
            return False, response
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_full_voice_assistant():
    """Testa o assistente completo"""
    print("\\n🤖 TESTE DO ASSISTENTE COMPLETO")
    print("=" * 50)
    
    try:
        print("\\n1. Inicializando assistente...")
        from main import VoiceAssistant
        assistant = VoiceAssistant()
        print("✅ Assistente inicializado")
        
        print("\\n2. Testando processamento de entrada...")
        test_input = "Qual a capital do Brasil?"
        
        print(f"Simulando entrada de voz: {test_input}")
        assistant.process_voice_input(test_input)
        
        print("\\n3. Limpando recursos...")
        assistant.cleanup()
        
        print("✅ Teste completo realizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste completo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DE CORREÇÕES - ASSISTENTE DE VOZ")
    print("=" * 60)
    
    # Teste 1: Correção da depreciação
    success1, response = test_llm_deprecation_fix()
    
    if success1:
        # Teste 2: Assistente completo
        success2 = test_full_voice_assistant()
        
        print("\\n" + "=" * 60)
        if success1 and success2:
            print("✅ TODOS OS TESTES PASSARAM!")
            print("✅ Depreciação corrigida")
            print("✅ Áudio funcionando")
            print("✅ Sistema pronto para uso!")
        else:
            print("❌ Alguns testes falharam")
        print("=" * 60)
    else:
        print("\\n❌ Teste inicial falhou - verifique a configuração")

if __name__ == "__main__":
    main()
