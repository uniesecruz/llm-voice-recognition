"""
Módulo para síntese de voz usando gTTS e reprodução com pygame
"""
from gtts import gTTS
import pygame
import tempfile
import os
from io import BytesIO
from typing import Optional

class VoiceSynthesizer:
    """Classe para síntese e reprodução de voz"""
    
    def __init__(self, language: str = 'pt-br'):
        """
        Inicializa o sintetizador de voz
        
        Args:
            language (str): Código do idioma para síntese (ex: 'pt-br', 'en')
        """
        self.language = language
        
        # Inicializa o pygame mixer para reprodução de áudio
        pygame.mixer.init()
        
        print(f"Sintetizador de voz inicializado (idioma: {language})")
    
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
            
            # Cria um arquivo temporário para salvar o áudio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file_path = temp_file.name
            
            # Salva o áudio no arquivo temporário
            tts.save(temp_file_path)
            
            # Reproduz o áudio
            self._play_audio(temp_file_path)
            
            # Remove o arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
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
            
            print("Reprodução concluída!")
            
        except Exception as e:
            print(f"Erro ao reproduzir áudio: {e}")
    
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
            
            # Salva temporariamente para o pygame (que não suporta streams diretos)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_buffer.getvalue())
                temp_file_path = temp_file.name
            
            # Reproduz o áudio
            self._play_audio(temp_file_path)
            
            # Remove o arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
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
    
    def cleanup(self):
        """Limpa os recursos do pygame"""
        pygame.mixer.quit()
        print("Recursos de áudio liberados.")
