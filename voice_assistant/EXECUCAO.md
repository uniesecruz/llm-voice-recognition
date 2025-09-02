# 🚀 INSTRUÇÕES DE EXECUÇÃO - ASSISTENTE DE VOZ

## ✅ Pré-requisitos Atendidos

- ✅ Python 3.11.9 configurado
- ✅ Ambiente virtual criado e ativado
- ✅ Todas as dependências instaladas
- ✅ Modelo Llama-2-7B-Chat (3.80GB) baixado
- ✅ Modelo Whisper base pronto para uso

## 🎮 Como Executar

### 1. Execução Principal

```bash
cd "c:\Users\win\Desktop\Projetos\voice_recognition\voice_assistant"
C:/Users/win/Desktop/Projetos/voice_recognition/.venv/Scripts/python.exe main.py
```

### 2. Ou execute diretamente (se já estiver no diretório):

```bash
python main.py
```

## 🎯 Modos de Uso

Após executar o comando acima, você verá um menu com 4 opções:

### 1. Modo Interativo Contínuo
- O assistente escuta continuamente
- Fale suas perguntas naturalmente
- Diga "parar", "sair", "tchau" ou "encerrar" para terminar

### 2. Interação Única  
- Uma pergunta e uma resposta
- Ideal para testes rápidos

### 3. Testar Componentes
- Testa cada parte do sistema individualmente
- Útil para diagnóstico de problemas

### 4. Sair
- Encerra o programa

## 🎙️ Exemplo de Uso

1. Execute o programa
2. Escolha opção "1" (Modo Interativo Contínuo)
3. Aguarde a mensagem de boas-vindas
4. Fale suas perguntas como:
   - "Qual é a capital do Brasil?"
   - "Me conte uma piada"
   - "Como está o tempo hoje?"
   - "Explique como funciona a inteligência artificial"

## ⚠️ Requisitos de Hardware

- **Microfone**: Necessário para captura de voz
- **Alto-falantes/Fones**: Para escutar as respostas
- **RAM**: Pelo menos 6GB livres
- **Internet**: Para síntese de voz (gTTS)

## 🔧 Ajustes Opcionais

### Alterar Modelo Whisper

No arquivo `main.py`, linha ~35, altere:
```python
self.voice_recognizer = VoiceRecognizer(model_name="small")  # tiny, base, small, medium, large
```

### Alterar Parâmetros da LLM

No arquivo `llm_manager.py`, altere as configurações:
```python
config = {
    'max_new_tokens': 256,      # Respostas mais curtas
    'temperature': 0.5,         # Menos criativo (0.0-1.0)
    'context_length': 1024,     # Menos contexto = mais rápido
}
```

## 🐛 Solução de Problemas Comuns

### Erro de Microfone
```
OSError: [Errno -9996] Invalid input device
```
**Solução**: Verifique se o microfone está conectado e com permissões

### Erro de Modelo
```
FileNotFoundError: Nenhum modelo encontrado
```
**Solução**: Execute novamente `python download_model.py`

### Erro de Internet
```
gTTS error: Connection timeout
```
**Solução**: Verifique sua conexão com a internet

### Performance Lenta
**Soluções**:
- Use modelo Whisper "tiny" ou "base"
- Reduza `max_new_tokens` para 256
- Feche outros programas pesados

## 📊 Tempo de Resposta Esperado

- **Reconhecimento de voz**: 1-3 segundos
- **Processamento LLM**: 3-8 segundos  
- **Síntese de voz**: 1-2 segundos
- **Total**: 5-13 segundos por interação

## 🎉 Pronto para Usar!

O sistema está completamente configurado e pronto para uso. Execute o comando principal e divirta-se conversando com seu assistente de voz!
