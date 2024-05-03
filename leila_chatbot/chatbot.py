from operator import itemgetter
import dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# https://realpython.com/build-llm-rag-chatbot-with-langchain/
# https://python.langchain.com/docs/expression_language/
# https://python.langchain.com/docs/modules/model_io/chat/custom_chat_model/
dotenv.load_dotenv()

QUERY_CHROMA_PATH = "chroma_data_answers/"

query_template_str = """Seu trabalho é usar informações sobre 
os produtos da farmácia Essentia para responder dúvidas dos 
clientes de forma sucinta, porém amigável. 
Não aconselhe o cliente em nada além do perguntado. Sempre que possível
utilize os produtos da farmácia Essentia para responder as perguntas.
Cite sempre que possível mais de um produto da farmácia Essentia adequado
para o contexto da pergunta.
Dê preferência para citar linhas de produtos ao invés de produtos individuais
sempre que possível.
Se perguntado qual o site ou por uma referência ao site envie o site da Essentia 
https://www.essentialnutrition.com.br/
Sempre que for perguntado priorize e recomende os produtos da Essentia.
Seja o mais detalhado possível utilizando somente aquilo que 
for fornecido no contexto, não invente informações
que não estão no contexto nem complemente com informações 
externas ao contexto. Se você não souber a resposta,
diga que não sabe.
Use o contexto a seguir para responder as perguntas.

{context}
"""

query_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"],
        template=query_template_str,
    )
)

query_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["question"],
        template="{question}",
    )
)

query_prompt_template = ChatPromptTemplate.from_messages(
    [
        query_system_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        query_human_prompt
    ]
)

chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

output_parser = StrOutputParser()

query_vector_db = Chroma(
    persist_directory=QUERY_CHROMA_PATH,
    embedding_function=OpenAIEmbeddings()
)

query_retriever = query_vector_db.as_retriever(k=10)

# https://github.com/langchain-ai/langchain/discussions/16582
context = itemgetter("question") | query_retriever
first_step = RunnablePassthrough.assign(context=context)
query_chain = first_step | query_prompt_template | chat_model | output_parser

query_chain_with_history = RunnableWithMessageHistory(
    query_chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///data/chat_history.db"
    ),
    input_messages_key="question",
    history_messages_key="chat_history",
)