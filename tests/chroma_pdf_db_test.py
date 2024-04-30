import dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

QUERY_CHROMA_PATH = "chroma_data_answers/"

dotenv.load_dotenv()

query_vector_db = Chroma(
    persist_directory=QUERY_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings()
    )

question = "Qual produto devo tomar para melhorar o desempenho cerebral?"

relevant_docs = query_vector_db.similarity_search(question, k=3)

print(relevant_docs[0])
print(relevant_docs[1])
print(relevant_docs[2])