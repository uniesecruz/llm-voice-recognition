"""
Teste específico para síntese de voz - verifica se as correções resolveram o problema
"""
import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_synthesizer import VoiceSynthesizer

def test_voice_synthesis():
    """Testa a síntese de voz com as correções implementadas"""
    print("🔊 TESTE DE SÍNTESE DE VOZ")
    print("=" * 40)
    
    try:
        # Inicializa o sintetizador
        print("\\n1. Inicializando sintetizador...")
        synthesizer = VoiceSynthesizer(language='pt-br', volume=0.8)
        
        # Teste 1: Método padrão
        print("\\n2. Testando método padrão...")
        text1 = "Testando o método padrão de síntese de voz."
        success1 = synthesizer.text_to_speech(text1)
        print(f"Resultado método padrão: {'✅ Sucesso' if success1 else '❌ Falha'}")
        
        # Teste 2: Método stream
        print("\\n3. Testando método stream...")
        text2 = "Testando o método stream de síntese de voz."
        success2 = synthesizer.text_to_speech_stream(text2)
        print(f"Resultado método stream: {'✅ Sucesso' if success2 else '❌ Falha'}")
        
        # Teste 3: Múltiplas chamadas rápidas
        print("\\n4. Testando múltiplas chamadas...")
        for i in range(3):
            text = f"Esta é a mensagem número {i+1} de três."
            success = synthesizer.text_to_speech(text)
            print(f"Mensagem {i+1}: {'✅' if success else '❌'}")
        
        # Teste 4: Texto longo
        print("\\n5. Testando texto mais longo...")
        long_text = """Este é um teste com um texto mais longo para verificar 
        se o sistema consegue lidar com sínteses maiores sem problemas de arquivos temporários. 
        O sistema agora deve gerenciar melhor os recursos e evitar conflitos."""
        
        success_long = synthesizer.text_to_speech(long_text)
        print(f"Resultado texto longo: {'✅ Sucesso' if success_long else '❌ Falha'}")
        
        # Cleanup
        print("\\n6. Limpando recursos...")
        synthesizer.cleanup()
        
        print("\\n" + "=" * 40)
        if all([success1, success2, success_long]):
            print("✅ TODOS OS TESTES DE ÁUDIO PASSARAM!")
            print("✅ Problema de arquivos temporários resolvido!")
        else:
            print("❌ Alguns testes falharam.")
        print("=" * 40)
        
    except Exception as e:
        print(f"\\n❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voice_synthesis()
