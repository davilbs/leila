from leila_chatbot.chatbot import query_chain

while(True):
    question = input("Digite sua pergunta: ")
    print("Resposta:", query_chain.invoke(question))
    print()