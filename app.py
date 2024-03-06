#チャットボットのUIを表示するためのファイル
#このファイルを実行すると、ブラウザが立ち上がり、チャットボットのUIが表示される
import streamlit as st
from do_rag import do_rag
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from IPython.display import display, HTML


st.header("Chat bot app")

#チャット履歴のメモリを作成する
chat_history = StreamlitChatMessageHistory(key="chat_history")

#チャット履歴を表示する
for chat in chat_history.messages:
    st.chat_message(chat.type).write(chat.content)

#チャットの表示と入力を行う
if prompt:= st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)
    answer, image_html = do_rag(prompt)

    with st.chat_message("assistant"):
        st.write(answer)
    if image_html:
        display(HTML(image_html))

    #チャット履歴に追加する
    chat_history.add_messages(
        [
            HumanMessage(content=prompt),
            AIMessage(content=answer),
        ]
    )
