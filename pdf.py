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


#PDFを加工する関数を作成する
def process_pdf(file):
    #PDFから要素を取得する
    raw_pdf_elements = partition_pdf(
        filename=path + file,
        languages=["jpn"],
        extract_images_in_pdf=True, 
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combile_text_under_n_chars=2000,
        analyzed_image_output_dir_path=path + "output/", #これが上手くいかない（指定したパスに画像が保存されない→figureディレクトリに保存される）
    )
    #小さなサイズのファイルを削除する
    delete_small_files(path + "output/")

    #テーブル要素とテキスト要素を取得する
    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            texts.append(str(element))
    #テーブル要素とテキスト要素を返す
    return tables, texts


#小さなサイズのファイルを削除する関数を作成する
def delete_small_files(directory_path, max_size_kb=20):
    max_size_bytes = max_size_kb * 1024
    for filename in os.listdir(directory_path):
        #ファイルパスを取得する
        file_path = os.path.join(directory_path, filename)
        #ファイルが存在する場合
        if os.path.isfile(file_path):   
            file_size = os.path.getsize(file_path)
            #ファイルサイズが指定したサイズ以下の場合→ファイルを消去する
            if file_size <= max_size_bytes:
                os.remove(file_path)
                print(f"Deleted {file_path}")


#base64エンコードした画像と画像の要約テキストをリストに追加する関数を作成する
def summarize_images():
    img_base64_list = [] #画像をbase64形式で格納するリスト
    image_summaries = [] #画像の要約を格納するリスト
    img_prompt = "画像を日本語で詳細に説明してください" #画像の要約を取得するためのプロンプト

    for img_file in sorted(os.listdir(path + "figures/")):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(path + "figures/", img_file) #画像のパスを取得する
            base64_image = encode_image(img_path) #画像をbase64形式に変換する
            img_base64_list.append(base64_image) #画像をbase64形式でリストに追加する
            image_summaries.append(image_summarize(base64_image, img_prompt)) #画像の要約をリストに追加する

    return img_base64_list, image_summaries 

#画像をbase64形式に変換する関数を作成する
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#画像をテキストで要約して返す関数を作成する
def image_summarize(img_base64, prompt):
    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
    msg = chat.invoke([
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {img_base64}"}}
        ])
    ])
    return msg.content


#テーブルの要約テキストを返す関数を作成する
def summarize_tables(tables):

    #プロンプトを作成する
    table_prompt = """あなたはテーブルの内容を説明する役割をもっています。
    (1)何に関してのテーブルなのか、
    (2)テーブルの詳細内容と考察
    に関して日本語で説明してください。
    
    テーブル（テキスト）：
    {element}
    """
    prompt = ChatPromptTemplate.from_template(table_prompt)
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    #テーブルの要約テキストを取得する
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()
    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})
    assert len(table_summaries) == len(tables), "Summary tables and original tables should have the same length"

    return table_summaries