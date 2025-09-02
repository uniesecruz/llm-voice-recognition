"""
Módulo para síntese de voz usando gTTS e reprodução com pygame
"""
from gtts import gTTS
import pygame
import tempfile
import os
import time
import shutil
from io import BytesIO
from typing import Optional

class VoiceSynthesizer:
    """Classe para síntese e reprodução de voz"""
    
    def __init__(self, language: str = 'pt-br', volume: float = 0.8):
        """
        Inicializa o sintetizador de voz
        
        Args:
            language (str): Código do idioma para síntese (ex: 'pt-br', 'en')
            volume (float): Volume da reprodução (0.0 a 1.0)
        """
        self.language = language
        self.volume = volume
        
        # Inicializa o pygame mixer para reprodução de áudio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.music.set_volume(self.volume)
        
        # Cria diretório temporário para arquivos de áudio
        self.temp_dir = tempfile.mkdtemp(prefix="voice_assistant_")
        
        print(f"Sintetizador de voz inicializado (idioma: {language}, volume: {volume})")
    
    def _safe_remove_file(self, file_path: str, max_attempts: int = 5):
        """
        Remove arquivo temporário de forma segura com múltiplas tentativas
        
        Args:
            file_path (str): Caminho do arquivo a ser removido
            max_attempts (int): Número máximo de tentativas
        """
        for attempt in range(max_attempts):
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
                    return True
            except (PermissionError, OSError) as e:
                if attempt < max_attempts - 1:
                    # Aguarda um pouco antes da próxima tentativa
                    time.sleep(0.1 * (attempt + 1))
                else:
                    print(f"⚠️ Não foi possível remover arquivo temporário após {max_attempts} tentativas: {e}")
        return False
    
    def _get_unique_temp_file(self) -> str:
        """
        Gera um caminho único para arquivo temporário
        
        Returns:
            str: Caminho para arquivo temporário único
        """
        import uuid
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        return os.path.join(self.temp_dir, filename)
    
    def text_to_speech(self, text: str, slow: bool = False) -> bool:
        """
        Converte texto em fala e reproduz o áudio
        
        Args:
            text (str): Texto a ser convertido em fala
            slow (bool): Se True, fala mais devagar
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            print(f"Convertendo texto em fala: {text}")
            
            # Cria o objeto gTTS
            tts = gTTS(text=text, lang=self.language, slow=slow)
            
            # Gera um arquivo temporário único
            temp_file_path = self._get_unique_temp_file()
            
            # Salva o áudio no arquivo temporário
            tts.save(temp_file_path)
            
            # Reproduz o áudio
            self._play_audio(temp_file_path)
            
            # Remove o arquivo temporário de forma segura
            self._safe_remove_file(temp_file_path)
            
            return True
            
        except Exception as e:
            print(f"Erro na síntese de voz: {e}")
            return False
    
    def _play_audio(self, audio_file_path: str):
        """
        Reproduz um arquivo de áudio usando pygame
        
        Args:
            audio_file_path (str): Caminho para o arquivo de áudio
        """
        try:
            print("Reproduzindo áudio...")
            
            # Carrega e reproduz o áudio
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()
            
            # Aguarda a reprodução terminar
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Aguarda um pouco mais para garantir que o arquivo seja liberado
            pygame.time.wait(200)
            
            # Para e descarrega o mixer para liberar o arquivo
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
            print("Reprodução concluída!")
            
        except Exception as e:
            print(f"Erro ao reproduzir áudio: {e}")
            # Tenta parar o mixer em caso de erro
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            except:
                pass
    
    def text_to_speech_stream(self, text: str, slow: bool = False) -> bool:
        """
        Converte texto em fala usando stream em memória (mais rápido)
        
        Args:
            text (str): Texto a ser convertido em fala
            slow (bool): Se True, fala mais devagar
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            print(f"Convertendo texto em fala (stream): {text}")
            
            # Cria o objeto gTTS
            tts = gTTS(text=text, lang=self.language, slow=slow)
            
            # Cria um buffer em memória
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Gera um arquivo temporário único
            temp_file_path = self._get_unique_temp_file()
            
            # Salva o buffer no arquivo temporário
            with open(temp_file_path, 'wb') as f:
                f.write(audio_buffer.getvalue())
            
            # Reproduz o áudio
            self._play_audio(temp_file_path)
            
            # Remove o arquivo temporário de forma segura
            self._safe_remove_file(temp_file_path)
            
            return True
            
        except Exception as e:
            print(f"Erro na síntese de voz (stream): {e}")
            return False
    
    def say_welcome(self):
        """Reproduz uma mensagem de boas-vindas"""
        welcome_text = "Olá! Eu sou seu assistente de voz. Como posso ajudá-lo hoje?"
        return self.text_to_speech(welcome_text)
    
    def say_goodbye(self):
        """Reproduz uma mensagem de despedida"""
        goodbye_text = "Até logo! Foi um prazer ajudá-lo."
        return self.text_to_speech(goodbye_text)
    
    def say_error(self):
        """Reproduz uma mensagem de erro"""
        error_text = "Desculpe, não consegui entender. Pode repetir, por favor?"
        return self.text_to_speech(error_text)
    
    def set_language(self, language: str):
        """
        Altera o idioma da síntese de voz
        
        Args:
            language (str): Novo código do idioma
        """
        self.language = language
        print(f"Idioma alterado para: {language}")
    
    def set_volume(self, volume: float):
        """
        Altera o volume da reprodução
        
        Args:
            volume (float): Volume (0.0 a 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))  # Garante que está entre 0 e 1
        pygame.mixer.music.set_volume(self.volume)
        print(f"Volume alterado para: {self.volume}")
    
    def speak_with_options(self, text: str, slow: bool = False, lang: str = None, volume: float = None) -> bool:
        """
        Fala um texto com opções personalizadas
        
        Args:
            text (str): Texto a ser falado
            slow (bool): Falar mais devagar
            lang (str): Idioma específico para esta fala
            volume (float): Volume específico para esta fala
            
        Returns:
            bool: True se bem-sucedido
        """
        # Salva configurações atuais
        original_lang = self.language
        original_volume = self.volume
        
        try:
            # Aplica configurações temporárias
            if lang:
                self.language = lang
            if volume is not None:
                self.set_volume(volume)
            
            # Fala o texto
            success = self.text_to_speech(text, slow)
            
            return success
            
        finally:
            # Restaura configurações originais
            self.language = original_lang
            if volume is not None:
                self.set_volume(original_volume)
    
    def cleanup(self):
        """Limpa os recursos do pygame e arquivos temporários"""
        try:
            # Para qualquer reprodução em andamento
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()
            
            # Remove diretório temporário e seus arquivos
            import shutil
            if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir)
                    print(f"Diretório temporário removido: {self.temp_dir}")
                except Exception as e:
                    print(f"⚠️ Erro ao remover diretório temporário: {e}")
            
            print("Recursos de áudio liberados.")
            
        except Exception as e:
            print(f"⚠️ Erro durante cleanup: {e}")
