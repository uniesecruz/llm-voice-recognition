"""
Módulo para reconhecimento de voz usando Whisper via SpeechRecognition
"""
import speech_recognition as sr
import whisper
import io
import wave
import tempfile
import os
from typing import Optional

class VoiceRecognizer:
    """Classe para reconhecimento de voz usando Whisper"""
    
    def __init__(self, model_name: str = "base"):
        """
        Inicializa o reconhecedor de voz
        
        Args:
            model_name (str): Nome do modelo Whisper a ser usado (tiny, base, small, medium, large)
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Carrega o modelo Whisper
        print(f"Carregando modelo Whisper '{model_name}'...")
        self.whisper_model = whisper.load_model(model_name)
        print("Modelo Whisper carregado com sucesso!")
        
        # Ajusta o reconhecedor para ruído ambiente
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibra o microfone para o ruído ambiente"""
        print("Calibrando microfone para ruído ambiente...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Calibração concluída!")
    
    def listen_for_speech(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Escuta e reconhece a fala do usuário
        
        Args:
            timeout (int): Tempo limite para começar a escutar (segundos)
            phrase_time_limit (int): Tempo limite para a frase (segundos)
            
        Returns:
            str: Texto reconhecido ou None se não conseguir reconhecer
        """
        try:
            print("Escutando... Fale alguma coisa!")
            
            # Escuta o áudio do microfone
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processando áudio...")
            
            # Converte o áudio para um formato que o Whisper pode processar
            audio_data = audio.get_wav_data()
            
            # Salva temporariamente o áudio em um arquivo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Usa o Whisper para transcrever o áudio
                result = self.whisper_model.transcribe(temp_file_path)
                text = result["text"].strip()
                
                if text:
                    print(f"Texto reconhecido: {text}")
                    return text
                else:
                    print("Nenhum texto foi reconhecido.")
                    return None
                    
            finally:
                # Remove o arquivo temporário
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except sr.WaitTimeoutError:
            print("Tempo limite atingido. Nenhuma fala detectada.")
            return None
            
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
            return None
            
        except Exception as e:
            print(f"Erro durante o reconhecimento de voz: {e}")
            return None
    
    def continuous_listen(self, callback_function, stop_phrases=None):
        """
        Escuta continuamente e chama uma função callback quando detecta fala
        
        Args:
            callback_function: Função a ser chamada com o texto reconhecido
            stop_phrases: Lista de frases que param a escuta contínua
        """
        if stop_phrases is None:
            stop_phrases = ["parar", "sair", "tchau"]
        
        print("Iniciando escuta contínua... Diga 'parar', 'sair' ou 'tchau' para encerrar.")
        
        while True:
            text = self.listen_for_speech()
            
            if text:
                # Verifica se é uma frase de parada
                if any(phrase.lower() in text.lower() for phrase in stop_phrases):
                    print("Encerrando escuta contínua...")
                    break
                
                # Chama a função callback com o texto reconhecido
                callback_function(text)
