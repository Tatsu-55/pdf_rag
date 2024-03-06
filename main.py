from pdf import process_pdf, summarize_tables, summarize_images
from retriever import create_vectorstore
from rag import rag_application


def main():
    #PDFを要素ごとに分解する（テキスト、テーブル、画像）
    tables, texts = process_pdf("input/test.pdf")

    #テーブルのサマリを作成する
    table_summaries = summarize_tables(tables)

    #画像のサマリを作成する
    img_base64_list, image_summaries = summarize_images()

    #Multivector Retrieverを作成する
    retriever = create_vectorstore(texts, table_summaries, image_summaries, tables, img_base64_list)

    #質問文を作成する
    questions = [
        "学習したデータに基づいて、報告書に関連する画像を何か一つ表示して"
    ]

    #クエリに対してRAGを実行する
    for query in questions:
        print(f"Q: {query}")
        result = rag_application(query, retriever)
        print(f"A: {result}\n\n")
        print("----------------------------------")

    
if __name__ == "__main__":
    main()