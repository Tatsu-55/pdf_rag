from langchain_community.vectorstores import Chroma
import chromadb
from langchain.storage import InMemoryStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from rag import rag_application
import pickle

docstore_filename = "./docstore.pickle"
collection_name = "multi_modal_rag_modified"
directory = "./sample_2"

#テスト用
def do_rag():

    client = chromadb.PersistentClient(path=directory)
    vectorstore = Chroma(collection_name=collection_name, embedding_function=OpenAIEmbeddings(), client=client)
    with open(docstore_filename, "rb") as file:
        docstore = pickle.load(file)

    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore, id_key='doc_id')
    
    #クエリに対してRAGを実行する(回答を返す)
    query = "Adansonsについて教えてください。"
    print(f"Q: {query}")
    result = rag_application(query, retriever)
    print(f"A: {result}\n\n")
    print("----------------------------------")
    return result

#RAGの実行だけを行う
if __name__ == "__main__":
    do_rag()