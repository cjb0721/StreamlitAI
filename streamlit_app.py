import streamlit as st
from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings

from utils import add_to_local, get_data_info, remove_file


def delete_file(item):
    st.session_state.files.pop(item["key"])
    remove_file(item["file"])


def init_data():
    info = get_data_info()
    st.session_state.files = {
        i+1: file_name
        for i, file_name in enumerate(info["files"])
    }
    return info


def add_knowledge():
    col_1, col_2 = st.columns(2)
    with col_1:
        uploaded_files = st.file_uploader(
            "Upload a file",
            type=["TXT", "CSV", "DOCX", "HTML"],
            accept_multiple_files=True
        )
        if st.button("Add to local"):
            msg = add_to_local(uploaded_files)
            if "Success" in msg and "Warning" in msg:
                st.success(msg["Success"])
                st.warning(msg["Warning"])
            elif "Success" in msg:
                st.success(msg)
            elif "Warning" in msg:
                st.warning(msg)
            elif "Error" in msg:
                st.error(msg)
            else:
                pass

    with col_2:
        st.text_input("Add an url")
        if st.button("Add url to local", type="primary"):
            st.info("Waiting TODO")


def chat():
    query = st.text_area("Ask a question")
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        button_ask = st.button("Ask")
    with col_2:
        button_count = st.button("Count Tokens")
    with col_3:
        button_clear = st.button("Clear History")
    st.markdown("---")

    if button_ask and query:
        # TODO 1.获取文件内容 2.获取答案 3.记录输入输出内容
        st.markdown(query)
    if button_count:
        # TODO 展示输入输出内容
        st.text_area("")
    if button_clear:
        # TODO 清除输出记录
        st.info("Clear success!")


def forget():
    col_1, col_2 = st.columns(2)
    data = init_data()
    with col_1:
        col_1.metric("Total Documents", data["len"])
        for file in data["files"]:
            st.button(f"✔️ {file}")

    with col_2:
        col_2.metric("Total Size (bytes)", data["total_size"])
        for index, file in enumerate(data["files"]):
            if (index + 1) in st.session_state.files:
                st.button(
                    '删除',
                    key=index + 1,
                    on_click=delete_file,
                    args=[{"key": index + 1, "file": file}]
                )


def init_home():
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
        layout="wide",
        menu_items={}
    )
    hide_default_format = """
       <style>
           footer {visibility: hidden;}
       </style>
   """
    st.caption(hide_default_format, unsafe_allow_html=True)
    st.write("# Welcome to Streamlit! 👋")
    st.markdown("---")
    genre = st.radio(
        "Choose an action",
        ("Add knowledge", "Chat with your brain", "Forget")
    )
    st.markdown("---")

    if genre == "Add knowledge":
        add_knowledge()

    elif genre == "Chat with your brain":
        chat()

    elif genre == "Forget":
        forget()


if __name__ == '__main__':
    init_home()
