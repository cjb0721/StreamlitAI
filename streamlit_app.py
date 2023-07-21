import streamlit as st
import openai

from utils import add_to_local, get_data_info, remove_file, embed_docs, text_to_docs, search_docs, get_answer


def delete_file(item):
    st.write(item,st.session_state.files)
    st.session_state.files.pop(item["key"])
    st.session_state.files_data.pop(item["file"])
    remove_file(item["file"])


def init_data():
    info = get_data_info()
    st.session_state.files = []
    st.session_state.files_data = {}
    for item in info["files"]:
        st.session_state.files.append(item["name"])
        st.session_state.files_data.update({item["name"]: item["body"]})
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
    st.write(st.session_state)

    if button_ask and query:
        # TODO 1.获取文件内容 2.获取答案 3.记录输入输出内容
        files_body_str = "\n".join(st.session_state.files_data.values())
        text = text_to_docs(files_body_str)
        st.markdown("---1")
        index = embed_docs(text)
        st.markdown("---2")
        sources = search_docs(index, query)
        st.markdown("---3")
        answer = get_answer(sources, query)
        st.markdown("---4")
        st.markdown(answer)
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
        col_1.metric("Total Documents", data["count"])
        for item in data["files"]:
            st.button(f"✔️ {item['name']}")

    with col_2:
        col_2.metric("Total Size (bytes)", data["total_size"])
        for item in data["files"]:
            st.button(
                '删除',
                key=item["index"],
                on_click=delete_file,
                args=[{"key": item["index"], "file": item["name"]}]
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

    openai.api_key = "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"

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    st.write(response)
    
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
    st.cache_data.clear()
    init_data()
    init_home()
