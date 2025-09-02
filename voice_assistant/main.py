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
        
        try:
            # Gera resposta usando a LLM
            print("🧠 Processando com IA...")
            response = self.llm_manager.generate_response(text)
            
            if response and response.strip():
                # Mostra a resposta no console
                print(f"🤖 Assistente responde: {response}")
                
                # GARANTE que a resposta seja convertida em áudio
                print("🔊 Iniciando conversão para áudio...")
                
                # Tenta múltiplas estratégias para garantir o áudio
                audio_success = False
                
                # Estratégia 1: Método padrão
                audio_success = self.convert_text_to_speech(response)
                
                # Estratégia 2: Se falhou, tenta quebrar em frases menores
                if not audio_success:
                    print("🔄 Tentando quebrar texto em frases menores...")
                    sentences = self._split_into_sentences(response)
                    
                    for i, sentence in enumerate(sentences):
                        if sentence.strip():
                            print(f"📢 Lendo frase {i+1}/{len(sentences)}: {sentence[:50]}...")
                            sentence_success = self.convert_text_to_speech(sentence.strip())
                            if sentence_success:
                                audio_success = True
                            # Pequena pausa entre frases
                            import time
                            time.sleep(0.5)
                
                # Estratégia 3: Se ainda falhou, tenta uma mensagem simplificada
                if not audio_success:
                    simple_msg = "Resposta processada. Verifique o texto no console."
                    print("🔄 Tentando mensagem simplificada...")
                    audio_success = self.convert_text_to_speech(simple_msg)
                
                # Confirma se o áudio foi reproduzido
                if audio_success:
                    print("✅ Resposta reproduzida em áudio com sucesso!")
                else:
                    print("❌ Não foi possível reproduzir áudio. Resposta disponível apenas em texto.")
                    
            else:
                error_msg = "Desculpe, não consegui gerar uma resposta adequada."
                print(f"⚠️ {error_msg}")
                self.convert_text_to_speech(error_msg)
                
        except Exception as e:
            error_msg = f"Ocorreu um erro ao processar sua pergunta."
            print(f"❌ Erro: {str(e)}")
            self.convert_text_to_speech("Desculpe, ocorreu um erro interno.")
    
    def _split_into_sentences(self, text: str) -> list:
        """
        Divide o texto em frases menores para facilitar a síntese
        
        Args:
            text (str): Texto a ser dividido
            
        Returns:
            list: Lista de frases
        """
        import re
        # Divide por pontos, exclamações e interrogações
        sentences = re.split(r'[.!?]+', text)
        # Remove frases vazias e muito curtas
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    def convert_text_to_speech(self, text: str) -> bool:
        """
        Converte qualquer texto em fala com tratamento de erro
        
        Args:
            text (str): Texto a ser convertido em fala
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            print(f"🔊 Convertendo em áudio: {text[:100]}{'...' if len(text) > 100 else ''}")
            
            # Primeira tentativa com método padrão
            success = self.voice_synthesizer.text_to_speech(text)
            
            if success:
                print("✅ Áudio reproduzido com sucesso!")
                return True
            else:
                print("⚠️ Falha na primeira tentativa, tentando método alternativo...")
                # Segunda tentativa com método stream
                success = self.voice_synthesizer.text_to_speech_stream(text)
                
                if success:
                    print("✅ Áudio reproduzido com método alternativo!")
                    return True
                else:
                    print("❌ Falha em ambos os métodos de síntese de voz")
                    # Terceira tentativa com configurações diferentes
                    print("⚠️ Tentando com configurações alternativas...")
                    success = self.voice_synthesizer.speak_with_options(text, slow=True, volume=0.9)
                    
                    if success:
                        print("✅ Áudio reproduzido com configurações alternativas!")
                        return True
                    else:
                        print("❌ Todas as tentativas de síntese falharam")
                        return False
                    
        except Exception as e:
            print(f"❌ Erro na conversão texto-fala: {e}")
            # Última tentativa com método mais simples
            try:
                print("🔄 Tentativa final com método básico...")
                return self.voice_synthesizer.text_to_speech(text)
            except:
                return False
    
    def read_text_aloud(self, text: str):
        """
        Função pública para ler qualquer texto em voz alta
        
        Args:
            text (str): Texto a ser lido
        """
        print(f"\\n📖 Lendo texto: {text}")
        self.convert_text_to_speech(text)
    
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
    
    def read_custom_text(self):
        """Permite ao usuário digitar texto para ser convertido em fala"""
        print("\\n📝 LEITURA DE TEXTO PERSONALIZADO")
        print("-" * 40)
        
        try:
            while True:
                print("\\nOpções:")
                print("1. Digitar texto para leitura")
                print("2. Ler arquivo de texto")
                print("3. Voltar ao menu principal")
                
                option = input("\\nEscolha uma opção (1-3): ").strip()
                
                if option == "1":
                    # Leitura de texto digitado
                    text = input("\\nDigite o texto que deseja ouvir: ").strip()
                    
                    if text:
                        print(f"\\n📖 Lendo: {text[:100]}{'...' if len(text) > 100 else ''}")
                        self.convert_text_to_speech(text)
                    else:
                        print("⚠️ Texto vazio. Tente novamente.")
                
                elif option == "2":
                    # Leitura de arquivo
                    file_path = input("\\nDigite o caminho do arquivo de texto: ").strip()
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            
                        if content.strip():
                            print(f"\\n📄 Lendo arquivo: {file_path}")
                            print(f"Tamanho: {len(content)} caracteres")
                            
                            # Para textos muito longos, pergunta se quer continuar
                            if len(content) > 1000:
                                confirm = input(f"\\nO texto é longo ({len(content)} caracteres). Continuar? (s/n): ")
                                if confirm.lower() not in ['s', 'sim', 'y', 'yes']:
                                    continue
                            
                            self.convert_text_to_speech(content)
                        else:
                            print("⚠️ Arquivo vazio.")
                            
                    except FileNotFoundError:
                        print(f"❌ Arquivo não encontrado: {file_path}")
                    except Exception as e:
                        print(f"❌ Erro ao ler arquivo: {e}")
                
                elif option == "3":
                    break
                    
                else:
                    print("⚠️ Opção inválida. Tente novamente.")
                    
        except KeyboardInterrupt:
            print("\\n⚠️ Operação cancelada pelo usuário.")
        except Exception as e:
            print(f"\\n❌ Erro durante leitura personalizada: {e}")
    
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
            print("4. Ler Texto Personalizado")
            print("5. Sair")
            print("=" * 40)
            
            choice = input("\\nDigite sua escolha (1-5): ").strip()
            
            if choice == "1":
                assistant.run_interactive_mode()
            elif choice == "2":
                assistant.run_single_interaction()
            elif choice == "3":
                assistant.test_components()
            elif choice == "4":
                assistant.read_custom_text()
            elif choice == "5":
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
