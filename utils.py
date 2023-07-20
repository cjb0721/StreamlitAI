import os
import uuid
import streamlit as st

from setting import DATA_DIR, OPEN_API_KEY

from typing import Any, Dict, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore
from langchain.vectorstores.faiss import FAISS
from openai.error import AuthenticationError
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


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
                    st.session_state.files_data.update({uploaded_file.name: bytes_data.decode("utf8")})
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


def get_data_info():
    files = os.listdir(DATA_DIR)
    total_size = sum([
        os.path.getsize(os.path.join(DATA_DIR, name))
        for name in files
    ])
    info_dict = {
        "count": len(files),
        "total_size": total_size,
        "files": [
            {
                # "fid": uuid.uuid3(uuid.NAMESPACE_DNS, "test"),
                "index": index+1,
                "name": name,
                "body": get_file_data(name)
            }
            for index, name in enumerate(files)
        ],
    }
    return info_dict


def remove_file(file_name):
    return os.remove(os.path.join(DATA_DIR, file_name))


def get_file_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "r", encoding="utf8") as f:
        data = f.read()
    return data


def text_to_docs(text: str | List[str]) -> List[Document]:
    """Converts a string or list of strings to a list of Documents
    with metadata."""
    if isinstance(text, str):
        # Take a single string as one page
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
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks


def embed_docs(docs: List[Document]) -> VectorStore:
    """Embeds a list of Documents and returns a FAISS index"""
    # Embed the chunks
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPEN_API_KEY
    )  # type: ignore
    index = FAISS.from_documents(docs, embeddings)

    return index


def search_docs(index: VectorStore, query: str) -> List[Document]:
    """Searches a FAISS index for similar chunks to the query
    and returns a list of Documents."""

    # Search for similar chunks
    docs = index.similarity_search(query, k=5)
    return docs


def get_answer(docs: List[Document], query: str) -> Dict[str, Any]:
    """Gets an answer to a question from a list of Documents."""

    # Get the answer
    template = """Create a final answer to the given questions using the provided document excerpts(in no particular order) as references. ALWAYS include a "SOURCES" section in your answer including only the minimal set of sources needed to answer the question. If you are unable to answer the question, simply state that you do not know. Do not attempt to fabricate an answer and leave the SOURCES section empty.

    ---------

    QUESTION: What  is the purpose of ARPA-H?
    =========
    Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
    Source: 1-32
    Content: While we’re at it, let’s make sure every American can get the health care they need. \n\nWe’ve already made historic investments in health care. \n\nWe’ve made it easier for Americans to get the care they need, when they need it. \n\nWe’ve made it easier for Americans to get the treatments they need, when they need them. \n\nWe’ve made it easier for Americans to get the medications they need, when they need them.
    Source: 1-33
    Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. \n\nWe need to extend that same care to all Americans. \n\nThat’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
    Source: 1-30
    =========
    FINAL ANSWER: The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
    SOURCES: 1-32

    ---------

    QUESTION: {question}
    =========
    {summaries}
    =========
    FINAL ANSWER:"""

    chain = load_qa_with_sources_chain(
        OpenAI(
            temperature=0,
            openai_api_key=OPEN_API_KEY
        ),  # type: ignore
        chain_type="stuff",
        prompt=PromptTemplate(template=template, input_variables=["summaries", "question"]),
    )

    # Cohere doesn't work very well as of now.
    # chain = load_qa_with_sources_chain(
    #     Cohere(temperature=0), chain_type="stuff", prompt=STUFF_PROMPT  # type: ignore
    # )
    answer = chain(
        {"input_documents": docs, "question": query}, return_only_outputs=True
    )
    return answer
