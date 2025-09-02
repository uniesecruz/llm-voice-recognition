"""
Assistente de Voz Principal
Integra reconhecimento de voz, LLM e síntese de voz usando LangChain
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice_recognizer import VoiceRecognizer
from llm_manager import LLMManager
from voice_synthesizer import VoiceSynthesizer

class VoiceAssistant:
    """Classe principal do assistente de voz"""
    
    def __init__(self):
        """Inicializa o assistente de voz"""
        print("=" * 50)
        print("INICIALIZANDO ASSISTENTE DE VOZ")
        print("=" * 50)
        
        # Inicializa os componentes
        self.voice_recognizer = None
        self.llm_manager = None
        self.voice_synthesizer = None
        
        # Configura os componentes
        self._setup_components()
        
        print("=" * 50)
        print("ASSISTENTE DE VOZ PRONTO!")
        print("=" * 50)
    
    def _setup_components(self):
        """Configura todos os componentes do assistente"""
        
        try:
            # 1. Inicializa o reconhecedor de voz
            print("\\n1. Configurando reconhecimento de voz...")
            self.voice_recognizer = VoiceRecognizer(model_name="base")
            
            # 2. Inicializa o gerenciador da LLM
            print("\\n2. Configurando Large Language Model...")
            self.llm_manager = LLMManager()
            
            # 3. Inicializa o sintetizador de voz
            print("\\n3. Configurando síntese de voz...")
            self.voice_synthesizer = VoiceSynthesizer(language='pt-br')
            
            print("\\n✅ Todos os componentes configurados com sucesso!")
            
        except Exception as e:
            print(f"\\n❌ Erro ao configurar componentes: {e}")
            raise
    
    def process_voice_input(self, text: str):
        """
        Processa a entrada de voz do usuário
        
        Args:
            text (str): Texto reconhecido da fala do usuário
        """
        print(f"\\n🎙️ Usuário disse: {text}")
        
        # Gera resposta usando a LLM
        response = self.llm_manager.generate_response(text)
        
        # Converte a resposta em fala
        print(f"🤖 Assistente responde: {response}")
        self.voice_synthesizer.text_to_speech(response)
    
    def run_interactive_mode(self):
        """Executa o assistente em modo interativo contínuo"""
        print("\\n🎤 Iniciando modo interativo...")
        
        # Mensagem de boas-vindas
        self.voice_synthesizer.say_welcome()
        
        try:
            # Escuta contínua
            self.voice_recognizer.continuous_listen(
                callback_function=self.process_voice_input,
                stop_phrases=["parar", "sair", "tchau", "encerrar"]
            )
            
        except KeyboardInterrupt:
            print("\\n⚠️ Interrompido pelo usuário (Ctrl+C)")
        
        except Exception as e:
            print(f"\\n❌ Erro durante execução: {e}")
        
        finally:
            # Mensagem de despedida
            print("\\n👋 Encerrando assistente...")
            self.voice_synthesizer.say_goodbye()
            self.cleanup()
    
    def run_single_interaction(self):
        """Executa uma única interação com o usuário"""
        print("\\n🎤 Modo de interação única...")
        
        # Mensagem de boas-vindas
        self.voice_synthesizer.say_welcome()
        
        try:
            # Escuta uma única entrada
            text = self.voice_recognizer.listen_for_speech(timeout=10, phrase_time_limit=15)
            
            if text:
                self.process_voice_input(text)
            else:
                print("\\n⚠️ Nenhuma fala detectada.")
                self.voice_synthesizer.say_error()
                
        except Exception as e:
            print(f"\\n❌ Erro durante interação: {e}")
        
        finally:
            self.cleanup()
    
    def test_components(self):
        """Testa todos os componentes individualmente"""
        print("\\n🧪 TESTANDO COMPONENTES")
        print("-" * 30)
        
        try:
            # Teste da síntese de voz
            print("\\n1. Testando síntese de voz...")
            self.voice_synthesizer.text_to_speech("Teste de síntese de voz funcionando!")
            
            # Teste da LLM
            print("\\n2. Testando Large Language Model...")
            response = self.llm_manager.test_model()
            print(f"Resposta da LLM: {response}")
            
            # Teste do reconhecimento de voz
            print("\\n3. Testando reconhecimento de voz...")
            print("Fale algo nos próximos 5 segundos...")
            text = self.voice_recognizer.listen_for_speech(timeout=5, phrase_time_limit=10)
            
            if text:
                print(f"Texto reconhecido: {text}")
                print("\\n✅ Todos os testes passaram!")
            else:
                print("\\n⚠️ Nenhuma fala detectada no teste de reconhecimento.")
                
        except Exception as e:
            print(f"\\n❌ Erro durante os testes: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpa recursos utilizados"""
        if self.voice_synthesizer:
            self.voice_synthesizer.cleanup()
        print("\\n🧹 Recursos liberados.")

def main():
    """Função principal"""
    print("🤖 ASSISTENTE DE VOZ COM IA")
    print("Powered by LangChain + Whisper + Llama + gTTS\\n")
    
    try:
        # Verifica se o modelo foi baixado
        models_dir = Path("models")
        if not models_dir.exists() or not list(models_dir.glob("*.gguf")):
            print("❌ Modelo LLM não encontrado!")
            print("Execute primeiro: python download_model.py")
            return
        
        # Cria o assistente
        assistant = VoiceAssistant()
        
        # Menu de opções
        while True:
            print("\\n" + "=" * 40)
            print("ESCOLHA UMA OPÇÃO:")
            print("1. Modo Interativo Contínuo")
            print("2. Interação Única")
            print("3. Testar Componentes")
            print("4. Sair")
            print("=" * 40)
            
            choice = input("\\nDigite sua escolha (1-4): ").strip()
            
            if choice == "1":
                assistant.run_interactive_mode()
            elif choice == "2":
                assistant.run_single_interaction()
            elif choice == "3":
                assistant.test_components()
            elif choice == "4":
                print("\\n👋 Saindo...")
                break
            else:
                print("\\n⚠️ Opção inválida. Tente novamente.")
        
        # Limpeza final
        assistant.cleanup()
        
    except Exception as e:
        print(f"\\n❌ Erro fatal: {e}")
        print("\\nVerifique se todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
