class VertexRetriever:
    def __init__(self, vectorstore) -> None:
        self.vectorstore = vectorstore
        
    def get_retriever(self):
        self.retriever = self.vectorstore.as_retriever()
        return self.retriever
