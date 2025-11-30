# Gemini/Vertex AI Types
from google.genai.types import Retrieval, VertexRagStore

# Vertex AI SDK (RAG corpus)
import vertexai
from google import genai
from vertexai import rag
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval

from t_lib.t_project.t_config import ProjectConfig

class RetrievalRagTool:

    @staticmethod
    def get_retrieval_rag_tool():
        vertexai.init(project=ProjectConfig.project_id, location="us-east1")
        client = genai.Client(vertexai=True, project=ProjectConfig.project_id, location="us")

        # Currently supports Google first-party embedding models
        # fmt: off
        EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"  # @param {type:"string", isTemplate: true}
        # fmt: on

        # RAG Corpus Creation
        # Addresses the "Problem": "students... need to fulfill a robust rubric"
        # We ingest the rubric (rubrics.pdf) so the agents can evaluate against specific criteria.
        rag_corpus = rag.create_corpus(
            display_name="my-rag-corpus",
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=rag.RagEmbeddingModelConfig(
                    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                        publisher_model=EMBEDDING_MODEL
                    )
                )
            ),
        )

        rag.list_corpora()

        rag_file = rag.upload_file(
            corpus_name=rag_corpus.name,
            path=ProjectConfig.input_rubrics_file,
            display_name="test.md",
            description="my test file",
        )


        # Create a tool for the RAG Corpus

        rag_retrieval_tool = Retrieval(
                vertex_rag_store=VertexRagStore(
                    rag_corpora=[rag_corpus.name],
                    similarity_top_k=10,
                    vector_distance_threshold=0.5,
                )
            )
        ask_vertex_retrieval = VertexAiRagRetrieval(
            name='retrieve_rag_documentation',
            description=(
                'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
            ),
            rag_corpora=[rag_corpus.name],
            similarity_top_k=10,
            vector_distance_threshold=0.5,
        )
        print("RAG tool created successfully.")
        #return rag_retrieval_tool
        return ask_vertex_retrieval

