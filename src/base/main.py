import os
from urllib import response
from google import genai
from dotenv import load_dotenv

def iniciar_chat():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Erro: Chave de API não encontrada no arquivo .env")
        return None 


    config = genai.types.GenerateContentConfig(
        system_instruction=(
            """Responda somente em codigo morse com . e - apenas"""
        )
    )
    

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model='gemini-3.1-flash-lite-preview', config=config)
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