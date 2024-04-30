from leila_chatbot.chatbot import query_chain

context = "Nimesulida contem principios que podem levar pessoas alergicas a camarao a sofrer crises"
question = "Ha alguma contra indicacao para pessoas alergicas a camarao?"

print(query_chain.invoke({"context": context, "question": question}))

question = "Ha alguma contra indicacao para nimesulida?"

print(query_chain.invoke({"context": context, "question": question}))

question = "Qual o melhor tipo de tijolo para construir predios?"
print(query_chain.invoke({"context": context, "question": question}))