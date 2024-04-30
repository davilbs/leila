import dotenv
from langchain.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

PRODUCTS_JSON_PATH = "data/json_produtos_formatted.json"
ANSWERS_PDF_PATH = "data/answers_pdf.pdf"
PRODUCTS_CHROMA_PATH = "chroma_data"
ANSWERS_CHROMA_PATH = "chroma_data_answers"

dotenv.load_dotenv()

class JSONWrapper:
    def metadata_func(self, record: dict, metadata: dict) -> dict:
        metadata["product_name"] = record.get("name")
        metadata["product_price"] = record.get("price")
        metadata["nutritional_information"] = record.get("nutritional_info")
        
        return metadata

    def load_products(self):
        loader = JSONLoader(
                            file_path=PRODUCTS_JSON_PATH,
                            jq_schema=".items[]",
                            content_key="description",
                            metadata_func=self.metadata_func
                            )

        data = loader.load()

        query_vector_db = Chroma.from_documents(
            data,
            OpenAIEmbeddings(),
            persist_directory=PRODUCTS_CHROMA_PATH
        )

class PDFWrapper:
    def load_products(self):
        loader = PyPDFLoader(ANSWERS_PDF_PATH)

        pages = loader.load_and_split()

        query_vector_db = Chroma.from_documents(
            pages,
            OpenAIEmbeddings(),
            persist_directory=ANSWERS_CHROMA_PATH
        )

pdf_wrapper = PDFWrapper()
pdf_wrapper.load_products()