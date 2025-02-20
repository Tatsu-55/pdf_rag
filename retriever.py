from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
import uuid
import pickle
import chromadb

#vector storeに格納されたデータを永続化する設定を行う
persist_directory = "./sample_1"
collection_name = "multi_modal_rag"
docstore_filename = "./docstore.pickle"
client = chromadb.PersistentClient(path=persist_directory)
vectorstore = Chroma(collection_name=collection_name, embedding_function=OpenAIEmbeddings(), client=client)
docstore = InMemoryStore()


#ベクトルストアを生成する関数を作成する(テキスト、テーブル、画像の要素の追加を含む)
def create_vectorstore(texts, table_summaries, image_summaries, tables, img_base64_list):

    id_key='doc_id'
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=docstore, id_key=id_key)

    #テキストを追加する
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    for i, s in enumerate(texts):
        retriever.vectorstore.add_documents([Document(page_content=s, metadata={id_key: doc_ids[i]})])
    retriever.docstore.mset(list(zip(doc_ids, texts)))
    
    #テーブルのサマリと元要素を追加する
    table_ids = [str(uuid.uuid4()) for _ in texts]
    for i, s in enumerate(table_summaries):
        retriever.vectorstore.add_documents([Document(page_content=s, metadata={id_key: table_ids[i]})])
    retriever.docstore.mset(list(zip(table_ids, tables)))

    #画像のサマリと元要素を追加する
    img_ids = [str(uuid.uuid4()) for _ in img_base64_list]
    for i, s in enumerate(image_summaries):
        retriever.vectorstore.add_documents([Document(page_content=s, metadata={id_key: img_ids[i]})])
    retriever.docstore.mset(list(zip(img_ids, img_base64_list)))

    #ドキュメントストアをローカルで保存する
    pickle.dump(docstore, open(docstore_filename, "wb"))

    return retriever


