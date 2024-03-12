import os
import base64
import openai
import fitz
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate

#現段階はテキストの抽出のみを行う。画像の抽出はコードを記述するが、費用の観点から実装しない

#OpenAIのAPIキーを設定する
openai.api_key = os.environ["OPENAI_API_KEY"]
# テストに必要なファイルへのパス変数を指定する
path = "/Users/tatsu/products/pdf_multi_modal_rag/input/test.pdf"

#PDFを加工する関数を作成する
def process_pdf():
    doc = fitz.open(path)
    #PDFから要素を取得する
    texts = []
    for page in doc:
        text = page.get_text()
        texts.append(text)
    print("texts", texts)
    print("length", len(texts))
    print("texts[2]", texts[2])

    return  texts

if __name__ == "__main__":
    process_pdf()