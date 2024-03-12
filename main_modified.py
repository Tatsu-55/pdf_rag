from pdf_modified import process_pdf
from retriever_modified import create_vectorstore
from rag_modified import rag_application

path = "/Users/tatsu/products/pdf_multi_modal_rag/"
file = "input/test.pdf"

def main():
    #PDFを要素ごとに分解する（テキスト、テーブル、画像）
    texts = process_pdf(path, file)

    #Multivector Retrieverを作成する(テキスト要素のみ格納)
    retriever = create_vectorstore(texts)

    #質問文を作成する
    questions = [
        "東北大学みらい創造債について"
    ]

    #クエリに対してRAGを実行する
    for query in questions:
        print(f"Q: {query}")
        result = rag_application(query, retriever)
        print(f"A: {result}\n\n")
        print("----------------------------------")

    
if __name__ == "__main__":
    main()