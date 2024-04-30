from fastapi import FastAPI
from pydantic import BaseModel
import requests
from leila_chatbot.chatbot import query_chain


class Query(BaseModel):
    celnumber: str
    question: str


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/leila")
async def query_bot(query: Query):
    answer = query_chain.invoke(query.question)
    r = requests.post("https://graph.facebook.com/v19.0/267907706414033/messages",
                      headers={
                          "Authorization": "Bearer EAA2jh0CQx5oBOxWFgHF7J7w3eQr2rNQi8lrbyqYLOGrT1LeW60rxAG6k9lBQ6wQ0B2LqViuZAvqo8HmVUwPgiwfVpJSoaqMLSsmuYaogIV4B2m3NmXvPRrf8WD9i3GZBDA4JcRpMIyI8mAWgZCgNCSGIfCluF4q1SSkKh4KaKGyOfp2AIk5DZB5Qn5ZAy3s76bbHlPkWZCqEievcBgcf0ZD",
                          "Content-Type": "application/json"
                      },
                      json={
                          "messaging_product": "whatsapp",
                          "recipient_type": "individual",
                          "to": query.celnumber,
                          "type": "text",
                          "text": {
                              "preview_url": "false",
                              "body": answer
                          }
                      })
    print(r.text)
    return {"answer": answer}
