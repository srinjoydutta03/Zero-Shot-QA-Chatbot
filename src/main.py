import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
import re
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.web_research import WebResearchRetriever
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import AsyncHtmlLoader
from langchain_community.document_loaders import PDFMinerLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

def main():
    def get_response(query, chat_history):
        r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=0,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )
        vectorstore = Chroma(
            embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai"
        )
        question = query
        llm = ChatOpenAI(temperature=0)

        # Search
        search = GoogleSearchAPIWrapper(k=1)

        web_research_retriever = WebResearchRetriever.from_llm(
            vectorstore=vectorstore, llm=llm, search=search
        )
        try:
            web_research_retriever.invoke(question)
        except:
            pass

        res = search.results(question, 2)
        links = []
        for key, value in enumerate(res):
            links.append(str(value['link']))
            if links:
                for url in links:
                    if url.endswith('.pdf'):
                        vectorstore.add_documents(PDFMinerLoader(url, extract_images= False).load_and_split(r_splitter))
                        print("Add success!!")
        
        retriever = vectorstore.as_retriever()
        template = """Answer the question given the following contexts:
        {context}
        and
        Imagine three different experts are answering this question.
        They will brainstorm the answer step by step reasoning carefully and taking all facts into consideration
        All experts will write down 1 step of their thinking as step number cumulative to other steps taken by others without writing expert number,
        then share it with the group.
        They will each critique their response, and the all the responses of others
        They will check their answer based on science and the laws of physics, engineering, mathematics and medicine
        Then all experts will go on to the next step and write down this step of their thinking.
        They will keep going through steps until they reach their conclusion taking into account the thoughts of the other experts
        If at any time they realise that there is a flaw in their logic they will backtrack to where that flaw occurred
        If any expert realises they're wrong at any point then they acknowledges this and start another train of thought
        Each expert will assign a likelihood of their current assertion being correct
        Continue until the experts agree on the single most likely location
        And they write the answer in numerical format arrived from the calculations at the end.

        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        chain = RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x["question"]),
        "question": lambda x: x["question"],
        }) | prompt | llm | StrOutputParser()

        input = chain.invoke({"question": question})
        output_string = re.sub(r'(Expert \d+|All Experts): ', '', input)

        return output_string

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.set_page_config(
        page_title= "Homework Helper"
    )
    st.header("Your homework helper")

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    user_query = st.chat_input("Enter your question")

    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = get_response(user_query, st.session_state.chat_history)
            st.markdown(ai_response)

        st.session_state.chat_history.append(AIMessage(ai_response))
if __name__ == '__main__':
   main()