import os
import pickle
import streamlit as st
import langchain
from langchain import OpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import  load_qa_with_sources_chain

st.title('Talk with URLs')
st.sidebar.title('Enter the URLs to articles')

os.environ['OPENAI_API_KEY'] = st.sidebar.text_input('Enter OpenAI API Key')

urls = []
for i in range(3):
    url = st.sidebar.text_input(f'URL { i + 1}')
    urls.append(url)

process_urls_clicked = st.sidebar.button('Process URLs')
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()

if process_urls_clicked:
    #load data
    loader = UnstructuredURLLoader(urls = urls)
    main_placeholder.text('Data Loading Started ...')
    data = loader.load()

    #Split the data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 300, chunk_overlap= 15)
    main_placeholder.text('Document Splitting  Started ...')
    chunks = text_splitter.split_documents(data)

    #Create the embeddings
    embeddings = OpenAIEmbeddings()
    #Store embeddings in Vector Store
    main_placeholder.text('Processing the Embeddings into Vector DB ...')
    vectordb = FAISS.from_documents(chunks, embedding = embeddings)

    # Save the FAISS index to a pickle file
    with open(file_path, 'wb') as f:
        pickle.dump(vectordb,f)


query = main_placeholder.text_input('Question :')

if query:
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            vectordb = pickle.load(f)
            llm = OpenAI(temperature=0.9, max_tokens=256)
            chain = RetrievalQAWithSourcesChain.from_llm(llm = llm ,
                                                          retriever = vectordb.as_retriever())
            result = chain({'question' : query}, return_only_outputs= True)
            st.header('Answer')
            st.write(result['answer'])

            # Display Sources if Available

            sources = result.get('sources','')
            if sources:
                st.subheader('Sources')
                sources_list = sources.split('\n')
                for source in sources_list:
                    st.write(source)

