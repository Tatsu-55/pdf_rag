#チャットボットのUIを表示するためのファイル
#このファイルを実行すると、ブラウザが立ち上がり、チャットボットのUIが表示される
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from main_modified_exe import main

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
    answer = main(prompt)

    with st.chat_message("assistant"):
        st.write(answer)


    #チャット履歴に追加する
    chat_history.add_messages(
        [
            HumanMessage(content=prompt),
            AIMessage(content=answer),
        ]
    )
