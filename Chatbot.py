
import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI


OPENAI_API_KEY="sk-proj-10kIRJSZvKyVAFHs5xlj8sbqe94AHgJMVPcibxZUvpYiXw2b94amDZX2KN8kQ"
# OPENAI_API_KEY="sk-QV3FdRp8R6JMeX3CMUGT3BlnkFJFM3WaEuXKzjPnQ9kh40a"

st.header("My First Chatbot")
with st.sidebar:
    st.title("Your Documents")
    file=st.file_uploader("upload a PDF and start asking questions",type="pdf")
#Extract the text
#Break it into chunks
if file is not None:
    pdf_reader=PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()
        # st.write(text)

#Break it into chunks
    text_splitter=RecursiveCharacterTextSplitter(
    separators="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
    )
    chunks=text_splitter.split_text(text)
    #Generating Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    #Creating Vector store
    vector_store = FAISS.from_texts(chunks, embeddings)


    # get user question
    user_question = st.text_input("Type Your question here")


    # do similarity search
    if user_question:
        match = vector_store.similarity_search(user_question)
        # st.write(match)

        #define the LLM
        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-3.5-turbo"
        )


        #output results
        #chain -> take the question, get relevant document, pass it to the LLM, generate the output
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question = user_question)
        st.write(response)
