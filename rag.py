from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from base64 import b64decode
from IPython.display import display, HTML


#RAGを実行する関数を作成する
def rag_application(question, retriever):
    docs = retriever.get_relevant_documents(question) #質問に関連するチャンク文書を取ってくる
    print("docs", docs)
    docs_by_type = split_image_text_types(docs) 
    print(docs_by_type)

    image_html = None

    #ドキュメントのテキストをHTMLに変換する
    if len(docs_by_type["texts"]):
        for doc_id in docs_by_type["texts"]:
            doc = retriever.docstore.mget([doc_id])
            try:
                doc_html = convert_html(doc)
                display(HTML(doc_html))
            except Exception as e:
                print(doc)
    
    #出力する画像がある場合、それをHTMLで表示する
    if len(docs_by_type["images"]):
        image_html = plt_img_base64(docs_by_type["images"][0])
    
    model = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024, temperature=0, streaming=True)
    
    """チェーンを作成する
    1. retrieverで質問に関連するチャンクを検索し、画像とテキストに分類する
    2. RunnableLambda(generate_prompt)で、画像とテキストの出たからプロンプトを生成する
    3. chain.invokeメソッドを使ってRAGを実行する
    """
    chain = (
        {"context": retriever | RunnableLambda(split_image_text_types), "question": RunnablePassthrough()}
        | RunnableLambda(generate_prompt)
        | model
        | StrOutputParser()
    )
    answer = chain.invoke(question)

    return answer, image_html


#画像とテキストでタイプを分けてリストに追加する関数を作成する
def split_image_text_types(docs):
    b64 = []
    text = []
    for doc in docs:
        try:
            b64decode(doc)
            b64.append(doc)
        except Exception:
            text.append(doc)
    return {"images": b64, "texts": text}


#画像を表示する関数を作成する(image_htmlを返している)
def plt_img_base64(img_base64):
    image_html = f'<img src="data":image/jpeg;base64,{img_base64}>'
    display(HTML(image_html))
    return image_html


#テキストをHTMLに変換する関数を作成する
def convert_html(element):
    input_text = str(element)
    prompt_text = f"""
    回答例に倣って、テキストをHTMLテーブル形式に変換してください:

    テキスト:
    {input_text}

    回答例:
    項目 果物(kg) ナッツ(kg) 飲み物(L) 予想 45 20 15 60 実績 50 25 10 80
    差(実績-予想) 5 5 -5 -20
    →
    <table>
      <tr>
        <th>項目</th>
        <th>果物(kg)</th>
        <th>ナッツ(kg)</th>
        <th>飲み物(L)</th>
        ・・・
      </tr>
    </table>
    """
    message = HumanMessage(content=[
                {"type": "text", "text": prompt_text}
            ])
    model = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1024)
    response = model.invoke([message])
    return response.content


#プロンプトを生成する関数を作成する
def generate_prompt(dict):
        format_texts = "\n\n".join(dict["context"]["texts"])
        prompt_text = f"""
        以下の質問に基づいて回答を生成してください。
        回答は、提供された追加情報を考慮してください。

        質問: {dict["question"]}

        追加情報: {format_texts}
        """
        message_content = [{"type": "text", "text": prompt_text}]

        #画像が存在する場合のみ画像URLを追加する
        if dict["context"]["images"]:
            image_url = f"data:image/jpeg;base64,{dict['context']['images'][0]}"
            message_content.append({"type": "image_url", "image_url": {"url": image_url}})

        return [HumanMessage(content=message_content)]