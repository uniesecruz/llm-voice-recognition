# 🤖 Assistente de Voz com IA

Um assistente de voz completo que utiliza Whisper para reconhecimento de fala, Llama para processamento de linguagem natural e gTTS para síntese de voz, tudo orquestrado pelo LangChain.

## 🎯 Funcionalidades

- **Reconhecimento de Voz**: Utiliza OpenAI Whisper via SpeechRecognition para converter fala em texto
- **Processamento de Linguagem**: LLM Llama executando localmente via ctransformers
- **Síntese de Voz**: Google Text-to-Speech (gTTS) para converter texto em fala
- **Leitura de Texto**: Converte qualquer texto digitado ou arquivo em áudio
- **Orquestração**: LangChain para gerenciar o fluxo de processamento
- **Interface**: Modo interativo contínuo, interações únicas e leitura personalizada
- **Tratamento de Erros**: Sistema robusto de recuperação de falhas
- **Configurações**: Volume, velocidade e idioma ajustáveis

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Microfone funcional
- Conexão com internet (para gTTS)
- Aproximadamente 4GB de espaço livre em disco (para o modelo Llama)

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
git clone <url-do-repositorio>
cd voice_assistant
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\\Scripts\\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixe o modelo Llama

Execute o script de download do modelo:

```bash
python download_model.py
```

Este processo pode demorar alguns minutos dependendo da sua conexão com a internet.

## 🎮 Como Usar

### Execução Principal

```bash
python main.py
```

O programa apresentará um menu com as seguintes opções:

1. **Modo Interativo Contínuo**: O assistente escuta continuamente e responde às suas perguntas
2. **Interação Única**: Uma única pergunta e resposta
3. **Testar Componentes**: Testa cada componente individualmente
4. **Ler Texto Personalizado**: Converte texto digitado ou arquivos em áudio
5. **Sair**: Encerra o programa

### Leitura de Texto Personalizado

A nova funcionalidade permite:
- **Texto digitado**: Digite qualquer texto para conversão em áudio
- **Arquivo de texto**: Carregue arquivos .txt para leitura em voz alta
- **Exemplo**: Use o arquivo `exemplo_texto.txt` incluído para teste

### Comandos de Voz para Parar

No modo interativo contínuo, você pode dizer qualquer uma dessas palavras para encerrar:
- "parar"
- "sair" 
- "tchau"
- "encerrar"

## 🏗️ Estrutura do Projeto

```
voice_assistant/
├── main.py                 # Arquivo principal
├── voice_recognizer.py     # Módulo de reconhecimento de voz
├── llm_manager.py          # Gerenciador da LLM
├── voice_synthesizer.py    # Síntese de voz
├── download_model.py       # Script para baixar modelo
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
└── models/                # Pasta para modelos (criada automaticamente)
    └── llama-2-7b-chat.Q4_K_M.gguf
```

## 🔧 Configurações

### Modelo Whisper

Por padrão, usa o modelo "base". Você pode alterar no arquivo `main.py`:

```python
self.voice_recognizer = VoiceRecognizer(model_name="small")  # tiny, base, small, medium, large
```

### Idioma da Síntese

Por padrão configurado para português brasileiro. Para alterar:

```python
self.voice_synthesizer = VoiceSynthesizer(language='en')  # Para inglês
```

### Parâmetros da LLM

Edite o arquivo `llm_manager.py` para ajustar:

```python
config = {
    'max_new_tokens': 512,      # Tamanho máximo da resposta
    'temperature': 0.7,         # Criatividade (0.0 a 1.0)
    'context_length': 2048,     # Tamanho do contexto
    'repetition_penalty': 1.1,  # Penalidade por repetição
}
```

## 🛠️ Dependências Principais

- **speechrecognition**: Interface para reconhecimento de voz
- **openai-whisper**: Modelo de reconhecimento de voz da OpenAI
- **langchain**: Framework para aplicações com LLM
- **ctransformers**: Inferência de modelos transformer em CPU
- **gtts**: Google Text-to-Speech
- **pygame**: Reprodução de áudio
- **pyaudio**: Captura de áudio do microfone

## 🐛 Solução de Problemas

### Erro de Microfone

Se houver erro com o microfone:
1. Verifique se o microfone está conectado e funcionando
2. No Windows, verifique as permissões de microfone
3. Teste com outro aplicativo de gravação

### Modelo não encontrado

Se aparecer "Modelo LLM não encontrado":
1. Execute novamente: `python download_model.py`
2. Verifique se há espaço suficiente em disco
3. Verifique sua conexão com a internet

### Erro de áudio PyAudio

No Windows, se houver erro com PyAudio:
```bash
pip install pipwin
pipwin install pyaudio
```

### Síntese de voz não funciona

1. Verifique sua conexão com a internet (gTTS precisa de internet)
2. Teste os alto-falantes/fones de ouvido
3. Verifique se o pygame está funcionando

## 📊 Desempenho

- **Modelo Whisper base**: ~140MB, boa precisão
- **Modelo Llama Q4_K_M**: ~3.8GB, boa qualidade de resposta
- **Tempo de resposta**: 3-10 segundos dependendo do hardware
- **RAM necessária**: ~4-6GB durante execução

## 🤝 Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Faça commit das suas mudanças
4. Faça push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Agradecimentos

- OpenAI pelo modelo Whisper
- Meta pelo modelo Llama
- Google pelo gTTS
- Comunidade LangChain
- Todos os desenvolvedores das bibliotecas utilizadas

---

**Desenvolvido com ❤️ e Python**
