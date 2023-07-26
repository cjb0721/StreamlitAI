import streamlit as st
from utils import (
    add_to_local,
    get_knowledge,
    parse_sources,
    remove_file,
    embed_docs,
    text_to_docs,
    search_docs,
    get_chat_history,
    save_chat_history,
    clear_chat_history
)


def delete_file(file):
    st.session_state.knowledge["files"]["data"] = [
        item
        for item in st.session_state.knowledge["files"]["data"]
        if file["key"] != item["key"]
    ]
    remove_file(file["name"])


def init_data():
    st.session_state.knowledge = get_knowledge()
    st.session_state.chat_history = get_chat_history()


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

    if button_ask and query:
        contents = [
            item["content"]
            for item in st.session_state.knowledge["files"]["data"]
        ]
        docs = text_to_docs(contents)
        index = embed_docs(docs)
        sources = search_docs(index, query)
        answer = parse_sources(sources)
        st.markdown("---")
        st.markdown(answer)
        save_chat_history({"question": query, "answer": answer})

    if button_count:
        st.markdown("---")
        st.code(st.session_state.chat_history)
    if button_clear:
        clear_chat_history()
        st.markdown("---")
        st.info("Clear success!")


def forget():
    col_1, col_2 = st.columns(2)
    with col_1:
        col_1.metric(
            "Total Documents",
            st.session_state.knowledge["files"]["count"]
        )
        for item in st.session_state.knowledge["files"]["data"]:
            st.button(f"✔️ {item['name']}")

    with col_2:
        col_2.metric(
            "Total Size (bytes)",
            st.session_state.knowledge["files"]["total_size"]
        )
        for item in st.session_state.knowledge["files"]["data"]:
            st.button(
                '删除',
                key=item["key"],
                on_click=delete_file,
                args=[{"key": item["key"], "name": item["name"]}]
            )


def init_home():
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋",
        layout="wide",
        # menu_items={
        #     'Get Help': 'https://www.extremelycoolapp.com/help',
        #     'Report a bug': "https://www.extremelycoolapp.com/bug",
        #     'About': "# This is a header. This is an *extremely* cool app!"
        # }
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
    st.session_state.clear()
    init_data()
    init_home()
