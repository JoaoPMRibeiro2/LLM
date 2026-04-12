import os
from urllib import response
from google import genai
from dotenv import load_dotenv
## Codigo de teste para o modelo gemma-4-31b-it, com instruções de comportamento sem interface gráfica.

def iniciar_chat():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Erro: Chave de API não encontrada no arquivo .env")
        return None 


    config = genai.types.GenerateContentConfig(
        system_instruction=(
            "Você é o 'Guia de Saúde', um assistente virtual focado em pré-triagem e orientação. "
            "Seu objetivo é escutar os sintomas do usuário, fazer 1 ou 2 perguntas breves para esclarecer o quadro (se necessário), "
            "e então fornecer uma análise orientativa.\n\n"
            
            "SIGA ESTE FLUXO ESTRITAMENTE:\n"
            "1. Acolhimento: Seja empático e objetivo.\n"
            "2. Coleta: Entenda os sintomas principais.\n"
            "3. Hipóteses (NUNCA DIAGNÓSTICO): Liste de 2 a 3 condições ou causas comuns que costumam apresentar esses sintomas. "
            "Use frases como 'Sintomas assim costumam estar associados a quadros como...' ou 'Causas possíveis incluem...'.\n"
            "4. Encaminhamento: Diga qual especialidade médica o usuário deve procurar (ex: Cardiologista, Ortopedista, Clínico Geral).\n\n"
            
            "REGRAS DE SEGURANÇA INEGOCIÁVEIS:\n"
            "- Inclua SEMPRE este aviso em sua resposta final: '⚠️ *Aviso: Sou uma Inteligência Artificial. Esta análise é apenas informativa e não substitui uma consulta médica. Não inicie tratamentos por conta própria.*'\n"
            "- Se detectar sintomas de emergência (dor no peito, dormência súbita, falta de ar grave, confusão mental, sangramento intenso), "
            "PARE TUDO e instrua o usuário a ir IMEDIATAMENTE a um pronto-socorro ou ligar para a emergência local."
        ),
        temperature=0.3 # Temperatura baixa para respostas precisas e seguras
    )
    

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemma-4-31b-it', config=config)
    return client,chat

def pergunta(chat):
    
    consulta = input("\nVocê: ")
    
    while consulta.strip() == "":
        consulta = input("\nVocê (digite algo válido): ")
        
  
    resposta = chat.send_message(consulta)

    print(f"Agente: {resposta.text}\n")    

def menu():
    
    print("-----------------------\n Menu (Gpteculos 2.0) \n-----------------------")
    print("1. perguntar \n2. Novo Chat \n0. Sair\n")
    opcao = int(input("Opção: "))
    while (opcao > 2 or opcao < 0):
        opcao = int(input("Selecione uma opção válida: "))
    return opcao

def main():

    opcao = -1
    
    client, chat = iniciar_chat()
    
    while (opcao != 0):

        try:
            
            opcao = menu()

            match opcao:

                case 1:
                    pergunta(chat)
                
                case 2:
                    chat = client.chats.create(model='gemini-2.5-flash')
                    pergunta(chat)
                    
                case 0:
                    print("Saindo...")
                    
        except Exception as e:
                
            print(f"\nUm erro ocorreu: {e}")                
            
if __name__ == "__main__":
    main()