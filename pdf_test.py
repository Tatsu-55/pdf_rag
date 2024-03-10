import os
import base64
import openai
from unstructured.partition.pdf import partition_pdf
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate

#OpenAIのAPIキーを設定する
openai.api_key = os.environ["OPENAI_API_KEY"]
# テストに必要なファイルへのパス変数を指定する
path = "/Users/tatsu/products/pdf_multi_modal_rag/"
file = "input/test.pdf"

#PDFを加工する関数を作成する
def process_pdf(file):
    #PDFから要素を取得する
    raw_pdf_elements = partition_pdf(
        filename=path + file,
        languages=["jpn", "eng"], #日本語の言語を使用する(OCRの設の設定も含む)
        strategy="hi_res", #ストラテジーの設定
        extract_images_in_pdf=True,
        include_metadata=True, #メタデータを含める
        infer_table_structure=True,
        extract_image_block_types=["Image"], #画像のブロックタイプを指定する
        extract_image_block_to_payload=False,
        extract_image_block_output_dir=path + "figures/",
    )
    print("raw_pdf_element", raw_pdf_elements)
    #小さなサイズのファイルを削除する
    # delete_small_files(path + "figures/")

    #テーブル要素とテキスト要素を取得する
    tables = []
    texts = []
    others = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)): #テーブル要素を取得する(Table)
            tables.append(str(element))
        elif "unstructured.documents.elements.NarrativeText" in str(type(element)): #テキスト要素を取得する(NarrativeText)
            texts.append(str(element))
        else:
            others.append(str(element))
            
    #テーブル要素とテキスト要素を返す
    print("tables", tables)
    print("-------------------")
    print("texts", texts)
    print("-------------------")
    print("others", others)
    print("-------------------")
    return tables, texts, others

if __name__ == "__main__":
    tables, texts, others = process_pdf(file)