from rag_modified import rag_application
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
import pickle
import chromadb

path = "/Users/tatsu/products/pdf_multi_modal_rag/"
file = "input/test.pdf"

persist_directory = "./sample_3" 
collection_name = "multi_modal_rag_modified_3" 
docstore_filename = "./docstore_3.pickle" 
docstore = pickle.load(open(docstore_filename, "rb"))
client = chromadb.PersistentClient(path=persist_directory)
vectorstore = Chroma(collection_name=collection_name, embedding_function=OpenAIEmbeddings(), client=client)

def main(question):
    #Multivector Retrieverを作成する(テキスト要素のみ格納)
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore, id_key="doc_id")

    #入力された質問に対してRAGを実行する
    print(f"Q: {question}")
    result = rag_application(question, retriever)
    print(f"A: {result}\n\n")
    print("----------------------------------")
    return result
    
if __name__ == "__main__":
    main()