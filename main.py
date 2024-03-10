from pdf import process_pdf, summarize_tables
from retriever import create_vectorstore
from rag import rag_application


def main():
    #PDFを要素ごとに分解する（テキスト、テーブル、画像）
    tables, texts, others = process_pdf("input/test.pdf")

    #テーブルのサマリを作成する
    table_summaries = summarize_tables(tables)

    #画像のサマリを作成する
    #img_base64_list, image_summaries = summarize_images()
    img_base64_list, image_summaries = [], []

    #Multivector Retrieverを作成する
    retriever = create_vectorstore(texts, table_summaries, others, image_summaries, tables, img_base64_list)

    #質問文を作成する
    questions = [
        "参照系AIの開発に取り組んでいる学生は誰ですか？"
    ]

    #クエリに対してRAGを実行する
    for query in questions:
        print(f"Q: {query}")
        result = rag_application(query, retriever)
        print(f"A: {result}\n\n")
        print("----------------------------------")

    
if __name__ == "__main__":
    main()