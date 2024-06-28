import os
import re
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers.web_research import WebResearchRetriever
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VectorSearchVectorStore, VertexAIEmbeddings
from dotenv import load_dotenv
import openai
from langchain.schema.runnable import RunnableMap
from ..retriever import VertexRetriever

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

vector_store = VectorSearchVectorStore.from_components(
    project_id=os.environ.get("PROJECT_ID"),
    region=os.environ.get("REGION"),
    gcs_bucket_name=os.environ.get("BUCKET_NAME"),
    index_id=os.environ.get("INDEX_ID"),
    endpoint_id=os.environ.get("INDEX_ENDPOINT_ID"),
    embedding=VertexAIEmbeddings(model_name="textembedding-gecko@003", project=os.environ.get("PROJECT_ID")),
    stream_update=True,
)

def get_response(query):
    try:
        print("Starting get_response function")
        vr = VertexRetriever(vectorstore=vector_store)
        retriever = vr.get_retriever()
        print("reached here")
        # Use similarity_search to get similar documents
        similar_docs = None
        try:
            similar_docs = vector_store.similarity_search_with_score(query)
            print(f"Similar documents retrieved: ")
        except: 
            print("Similar docs not found")

        if (similar_docs == None) or all(score > 0.1 for (_, score) in similar_docs):
            # Only perform a search if the maximum similarity score is greater than 0.1
            print("Performing Google search for additional documents")
            search = GoogleSearchAPIWrapper(k=1)
            web_research_retriever = WebResearchRetriever.from_llm(
                vectorstore=vector_store, llm=ChatOpenAI(temperature=0), search=search
            )
            try:
                web_research_retriever.invoke(query)
            except Exception as e:
                print(f"Error during web research: {e}")
            
            res = search.results(query, 1)
            links = [result['link'] for result in res]
            print(f"Links found: {links}")
            for url in links:
                if url.endswith('.pdf'):
                    loader = PyPDFLoader(url)
                    pages = loader.load()
                    r_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1500,
                        chunk_overlap=0,
                        separators=["\n\n", "\n", "(?<=\. )", " ", ""]
                    )
                    doc_splits = r_splitter.split_documents(pages)
                    texts = [doc.page_content for doc in doc_splits]
                    metadatas = [doc.metadata for doc in doc_splits]
                    vector_store.add_texts(texts=texts, metadatas=metadatas, is_complete_overwrite=True)
                    print("New documents added successfully")

        # Use existing or newly added documents to form the response
        try:
            similar_docs = vector_store.similarity_search(query)
            print(f"Final similar documents: {similar_docs}")
        except:
            print("ERRROOORRRR")
        if not similar_docs:
            raise IndexError("No similar documents found.")
        
        context = [doc.page_content for doc in similar_docs]
        template = """Answer the question given the following contexts:
        {context}
        and
        Imagine three different experts are answering this question. They will brainstorm the answer step by step reasoning carefully.
        They will brainstorm the answer step by step reasoning carefully and taking all facts into consideration.
        They will each critique their response, and the all the responses of others.
        They will keep going through steps of their thoughts until they reach their conclusion taking into account the thoughts of the other experts.
        If at any time they realise that there is a flaw in their logic they will backtrack to where that flaw occurred.
        If any expert realises they're wrong at any point then they acknowledges this and start another train of thought
        Continue until the experts agree on the single most likely location. 
        And write the final right answer.
        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        chain = RunnableMap({
            "context": lambda x: context,
            "question": lambda x: x["question"],
        }) | prompt | ChatOpenAI(temperature=0) | StrOutputParser()

        response = chain.invoke({"question": query})
        output_string = re.sub(r'(Expert \d+|All Experts): ', '', response)

        print("Response generated successfully")
        return output_string
    except IndexError as e:
        print(f"Index error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

