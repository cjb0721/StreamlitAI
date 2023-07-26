import json
import os
import re
import uuid
from typing import List
from langchain.llms import AzureOpenAI
from setting import DATA_DIR, BASE_PATH
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter


def add_to_local(files):
    if not files:
        return "[Warning]: File is not None"
    new_files = []
    exist_files = []
    try:
        for uploaded_file in files:
            bytes_data = uploaded_file.read()
            file_path = os.path.join(DATA_DIR, uploaded_file.name)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(bytes_data.decode("utf8"))
                    new_files.append(uploaded_file.name)
            else:
                exist_files.append(uploaded_file.name)
        if new_files and not exist_files:
            return "[Success]: Add success"
        if not new_files and exist_files:
            return f"[Warning]: {', '.join(exist_files)} already exist"
        if new_files and exist_files:
            return {
                "Success": f"[Success]: {', '.join(new_files)} add success",
                "Warning": f"[Warning]: {', '.join(exist_files)} already exist"
            }
    except Exception as e:
        raise e


def get_knowledge() -> {}:
    files_name = os.listdir(DATA_DIR)
    files = {"data": []}
    total_size = 0
    count = 0
    for name in files_name:
        file_type = name.split(".")[-1]
        file_size = os.path.getsize(os.path.join(DATA_DIR, name))
        files["data"].append({
            "key": str(uuid.uuid1()),
            "name": name,
            "size": file_size,
            "type": file_type,
            "content": get_file_content(name)
        })
        total_size += file_size
        count += 1
    files["total_size"] = total_size
    files["count"] = count
    knowledge = {"files": files}
    return knowledge


def remove_file(file_name):
    return os.remove(os.path.join(DATA_DIR, file_name))


def get_file_content(file_name, path=DATA_DIR):
    file_path = os.path.join(path, file_name)
    with open(file_path, "r", encoding="utf8") as f:
        data = f.read()
    return data


def text_to_docs(text: str | List[str]) -> List[Document]:
    """
    Converts a string or list of strings to a list of Documents
    with metadata.
    """
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks


def embed_docs(docs: List[Document]):
    # Embed the chunks
    embeddings = OpenAIEmbeddings()
    index = VectorstoreIndexCreator(embedding=embeddings).from_documents(docs)
    return index


def search_docs(index, query: str):
    llm = AzureOpenAI(deployment_name="gpt-35-turbo", temperature=0)
    docs = index.query(query, llm=llm)
    return docs


def parse_sources(sources: str):
    first_one_sources = sources.split("\n")[0]
    re_first_one_sources = re.sub(r"<\|im_end\|>", "", first_one_sources)
    return re_first_one_sources.strip()


def get_chat_history():
    if os.path.exists(os.path.join(BASE_PATH, "chat_history.txt")):
        content = get_file_content("chat_history.txt", BASE_PATH)
        return content
    return None


def save_chat_history(chat):
    with open("chat_history.txt", "a", encoding="utf8") as f:
        f.write(f"{json.dumps(chat, ensure_ascii=False)}\n")


def clear_chat_history():
    if os.path.exists(os.path.join(BASE_PATH, "chat_history.txt")):
        return os.remove(os.path.join(BASE_PATH, "chat_history.txt"))
