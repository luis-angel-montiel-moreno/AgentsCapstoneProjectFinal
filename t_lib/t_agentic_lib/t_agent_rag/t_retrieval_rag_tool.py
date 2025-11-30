"""
RAG (Retrieval-Augmented Generation) Tool Module

This module implements the RAG infrastructure that enables agents to access
rubric criteria during document review. It uses Vertex AI to create a vector
database corpus from the rubric PDF, allowing agents to retrieve relevant
criteria sections when needed.

RAG Pattern:
Retrieval-Augmented Generation enhances LLM responses by grounding them in
retrieved context (the rubric), ensuring agents evaluate against actual
rubric standards rather than relying solely on training data.
"""

# Gemini/Vertex AI Types for RAG retrieval configuration
from google.genai.types import Retrieval, VertexRagStore

# Vertex AI SDK components for RAG corpus management
import vertexai
from google import genai
from vertexai import rag
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval

from t_lib.t_project.t_config import ProjectConfig

class RetrievalRagTool:
    """
    Factory class for creating and configuring the RAG retrieval tool.
    
    This class manages the RAG infrastructure that enables agents to access
    rubric criteria. It handles:
    - Vertex AI initialization and client setup
    - RAG corpus creation with vector database configuration
    - Rubric PDF ingestion into the corpus
    - RAG retrieval tool creation for agent use
    
    Addresses the "Problem": "students... need to fulfill a robust rubric"
    By ingesting the rubric PDF into a searchable vector database, agents can
    retrieve relevant rubric sections during review, ensuring evaluations align
    with actual rubric standards.
    """

    @staticmethod
    def get_retrieval_rag_tool():
        """
        Creates and configures the RAG retrieval tool for rubric access.
        
        This method performs the following steps:
        1. Initializes Vertex AI with project configuration
        2. Creates a RAG corpus with vector database backend
        3. Uploads the rubric PDF file into the corpus
        4. Creates a retrieval tool that agents can use to query the rubric
        
        The RAG corpus uses semantic search to find relevant rubric sections
        based on similarity, allowing agents to retrieve context-specific criteria
        when reviewing different aspects of student documents.
        
        Returns:
            VertexAiRagRetrieval: A tool instance that agents can use to retrieve
                rubric documentation during review
        
        Architecture:
        - Uses Vertex AI's managed RAG infrastructure for scalability
        - Employs text-embedding-005 model for semantic similarity search
        - Configures similarity thresholds to balance relevance and recall
        """
        # Initialize Vertex AI SDK with project configuration
        vertexai.init(project=ProjectConfig.project_id, location="us-east1")
        client = genai.Client(vertexai=True, project=ProjectConfig.project_id, location="us")

        # Embedding model configuration
        # Currently supports Google first-party embedding models
        # text-embedding-005 provides high-quality semantic embeddings for retrieval
        # fmt: off
        EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"  # @param {type:"string", isTemplate: true}
        # fmt: on

        # RAG Corpus Creation
        # Addresses the "Problem": "students... need to fulfill a robust rubric"
        # We ingest the rubric (rubrics.pdf) so the agents can evaluate against specific criteria.
        # The corpus acts as a vector database that enables semantic search over rubric content.
        rag_corpus = rag.create_corpus(
            display_name="my-rag-corpus",
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                        publisher_model=EMBEDDING_MODEL  # Uses text-embedding-005 for vector embeddings
                    )
                )
            ),
        )

        # List all existing corpora (useful for debugging and verification)
        rag.list_corpora()

        # Upload the rubric PDF file into the RAG corpus
        # This ingests the rubric document into the vector database, making it
        # searchable via semantic similarity queries from agents
        rag_file = rag.upload_file(
            corpus_name=rag_corpus.name,
            path=ProjectConfig.input_rubrics_file,  # Path to rubrics.pdf
            display_name="test.md",
            description="my test file",
        )

        # Create a Retrieval configuration object (alternative approach, currently unused)
        rag_retrieval_tool = Retrieval(
            vertex_rag_store=VertexRagStore(
                rag_corpora=[rag_corpus.name],
                similarity_top_k=10,              # Retrieve top 10 most similar chunks
                vector_distance_threshold=0.5,    # Maximum distance threshold for relevance
            )
        )
        
        # Create the VertexAiRagRetrieval tool for agent use
        # This tool enables agents to query the rubric corpus during document review
        ask_vertex_retrieval = VertexAiRagRetrieval(
            name='retrieve_rag_documentation',
            description=(
                'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
            ),
            rag_corpora=[rag_corpus.name],        # Corpus to search in
            similarity_top_k=10,                   # Return top 10 most relevant chunks
            vector_distance_threshold=0.5,        # Filter results by similarity threshold
        )
        print("RAG tool created successfully.")
        # Note: rag_retrieval_tool is an alternative implementation that's currently commented out
        #return rag_retrieval_tool
        return ask_vertex_retrieval

