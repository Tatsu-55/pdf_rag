from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage
from langchain.schema.output_parser import StrOutputParser



#RAGを実行する関数を作成する
def rag_application(question, retriever):
    docs = retriever.get_relevant_documents(question) #質問に関連するチャンク文書を取ってくる
    print("docs", docs)
    
    model = ChatOpenAI(model="gpt-3.5-turbo-0125", max_tokens=1024, temperature=0, streaming=True)
    
    """チェーンを作成する
    1. retrieverで質問に関連するチャンクを検索し、画像とテキストに分類する
    2. RunnableLambda(generate_prompt)で、画像とテキストの出たからプロンプトを生成する
    3. chain.invokeメソッドを使ってRAGを実行する
    """
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | RunnableLambda(generate_prompt)
        | model
        | StrOutputParser()
    )
    answer = chain.invoke(question)

    return answer

#プロンプトを生成する関数を作成する
def generate_prompt(dict):
        print("dict", dict)
        texts = dict['context']
        print("texts", texts)
        print("-------------------")
        formatted_texts = "\n\n".join(texts)
        print("formatted_texts", formatted_texts)
        print("-------------------")

        prompt_text = f"""
        以下の質問に基づいて回答を生成してください。
        回答は、提供された追加情報のうち、適切な情報を考慮してください。

        質問: {dict["question"]}

        追加情報: {formatted_texts}
        """
        print("prompt_text", prompt_text)
        message_content = [{"type": "text", "text": prompt_text}]

        return [HumanMessage(content=message_content)]