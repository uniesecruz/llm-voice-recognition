"""
Módulo para gerenciar a Large Language Model usando LangChain e ctransformers
"""
from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from pathlib import Path
import os

class LLMManager:
    """Classe para gerenciar a Large Language Model"""
    
    def __init__(self, model_path: str = None):
        """
        Inicializa o gerenciador da LLM
        
        Args:
            model_path (str): Caminho para o arquivo do modelo
        """
        if model_path is None:
            # Procura pelo modelo na pasta models
            models_dir = Path("models")
            model_files = list(models_dir.glob("*.gguf"))
            
            if not model_files:
                raise FileNotFoundError(
                    "Nenhum modelo encontrado na pasta 'models'. "
                    "Execute download_model.py primeiro para baixar um modelo."
                )
            
            model_path = str(model_files[0])
            print(f"Modelo encontrado: {model_path}")
        
        self.model_path = model_path
        self.llm = None
        self.chain = None
        
        # Carrega o modelo e configura a cadeia
        self._load_model()
        self._setup_chain()
    
    def _load_model(self):
        """Carrega o modelo LLM usando ctransformers"""
        print("Carregando modelo LLM...")
        
        # Configurações do modelo
        config = {
            'max_new_tokens': 512,
            'temperature': 0.7,
            'context_length': 2048,
            'repetition_penalty': 1.1,
        }
        
        try:
            self.llm = CTransformers(
                model=self.model_path,
                model_type="llama",
                config=config
            )
            print("Modelo LLM carregado com sucesso!")
            
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o modelo: {e}")
    
    def _setup_chain(self):
        """Configura a cadeia do LangChain com prompt personalizado"""
        
        # Template do prompt para o assistente
        prompt_template = """Você é um assistente de voz útil e amigável. Responda de forma clara, concisa e prestativa.
        
        Instruções:
        - Seja sempre educado e prestativo
        - Mantenha as respostas relativamente curtas (máximo 2-3 frases)
        - Se não souber algo, admita que não sabe
        - Responda sempre em português brasileiro
        
        Pergunta do usuário: {question}
        
        Resposta:"""
        
        # Cria o template de prompt
        prompt = PromptTemplate(
            input_variables=["question"],
            template=prompt_template
        )
        
        # Cria a cadeia LangChain usando a nova sintaxe recomendada
        self.chain = prompt | self.llm
        
        print("Cadeia LangChain configurada!")
    
    def generate_response(self, question: str) -> str:
        """
        Gera uma resposta para a pergunta do usuário
        
        Args:
            question (str): Pergunta do usuário
            
        Returns:
            str: Resposta gerada pela LLM
        """
        try:
            print(f"Processando pergunta: {question}")
            
            # Gera a resposta usando a nova sintaxe RunnableSequence
            response = self.chain.invoke({"question": question})
            
            # Limpa a resposta removendo espaços extras
            response = response.strip()
            
            print(f"Resposta gerada: {response}")
            return response
            
        except Exception as e:
            error_msg = f"Erro ao gerar resposta: {e}"
            print(error_msg)
            return "Desculpe, ocorreu um erro ao processar sua pergunta."
    
    def test_model(self):
        """Testa o modelo com uma pergunta simples"""
        test_question = "Olá, como você está?"
        print("Testando o modelo...")
        response = self.generate_response(test_question)
        return response
