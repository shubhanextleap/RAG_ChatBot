import os
import sys
import re
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(__file__))
from config import Config

class RAGEngine:
    def __init__(self):
        Config.validate()
        
        # Initialize Local BGE Embeddings
        print(f"Loading embedding model: {Config.EMBEDDING_MODEL_NAME}...")
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=Config.EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True},
            query_instruction="Represent this sentence for searching relevant passages:"
        )
        
        # Load Vector Store
        self.vector_db = Chroma(
            persist_directory=Config.CHROMA_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="hdfc_mutual_funds"
        )
        
        # Initialize LLM (Groq for high-speed factual inference)
        self.llm = ChatGroq(
            model=Config.GROQ_MODEL_NAME,
            groq_api_key=Config.GROQ_API_KEY,
            temperature=0
        )
        
        self.system_prompt = (
            "You are a factual FAQ assistant for HDFC Mutual Funds. "
            "Answer ONLY based on the provided context. If the answer is not in the context, "
            "state that you do not have that specific factual detail.\n\n"
            "STRICT CONSTRAINTS:\n"
            "1. Maximum 3 sentences per response.\n"
            "2. No investment advice, opinions, or 'best' fund recommendations.\n"
            "3. If asked for advice, say: 'I am a facts-only assistant and cannot provide investment advice.' "
            "Then provide this link: https://www.amfiindia.com/investor-corner\n"
            "4. End every response with exactly one source link from the metadata.\n"
            "5. Include a footer with the 'last_updated' date from the metadata.\n"
            "6. If the query asks about risk, specify the Riskometer rating (e.g., Very High, Moderately High).\n"
            "7. If the query asks about future performance or returns, explicitly redirect to the official factsheet link."
        )

    def _check_pii(self, text):
        """Detects PAN or Phone numbers to ensure privacy compliance."""
        pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        phone_pattern = r'\b\d{10}\b'
        if re.search(pan_pattern, text) or re.search(phone_pattern, text):
            return True
        return False

    def get_available_funds(self):
        """Retrieves a list of unique fund names from the ChromaDB metadata."""
        # ChromaDB's get method can retrieve metadata for all documents
        # We then extract unique fund_name values
        metadata_list = self.vector_db.get(include=['metadatas'])['metadatas']
        fund_names = sorted(list(set([m.get('fund_name') for m in metadata_list if m.get('fund_name')])))
        return fund_names

    def query(self, user_input, filter_fund=None):
        # 1. Privacy Guardrail
        if self._check_pii(user_input):
            return "For security reasons, please do not share personal identifiers like PAN or phone numbers. I cannot process this request."

        # 2. Retrieval with Relevance Threshold
        # Implementation of Metadata-Filtered Retrieval
        search_kwargs = {"k": 2}
        if filter_fund:
            search_kwargs["filter"] = {"fund_name": filter_fund}

        docs_with_scores = self.vector_db.similarity_search_with_relevance_scores(
            user_input, **search_kwargs
        )
        
        # Filter results (threshold set to 0.5 for BGE normalized scores)
        relevant_docs = [doc for doc, score in docs_with_scores if score > 0.5]
        
        if not relevant_docs:
            return ("I'm sorry, I couldn't find verified factual information regarding that query for the selected fund. "
                    "Please refer to https://www.hdfcfund.com/ for official details.")

        # 3. Context & Metadata Extraction
        context_content = "\n\n".join([d.page_content for d in relevant_docs])
        source_link = relevant_docs[0].metadata.get('source', 'https://groww.in')
        last_updated = relevant_docs[0].metadata.get('last_updated', 'Unknown')
        if 'T' in last_updated: last_updated = last_updated.split('T')[0]

        # 4. RAG Chain
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])

        chain = (
            {"context": lambda x: context_content, "question": RunnablePassthrough()}
            | prompt
            | self.llm
        )

        # 5. Generation & Formatting
        response = chain.invoke(user_input)
        answer = response.content

        # Ensure mandatory citation and footer
        final_response = (
            f"{answer}\n\n"
            f"Source: {source_link}\n"
            f"Last updated from sources: {last_updated}"
        )
        
        return final_response

if __name__ == "__main__":
    engine = RAGEngine()
    # Example Factual Query
    print(engine.query("What is the exit load for HDFC Mid Cap Fund?"))
    print("\n---\n")
    # Example Advisory Query
    print(engine.query("Which fund is better for me, HDFC Small Cap or Large Cap?"))