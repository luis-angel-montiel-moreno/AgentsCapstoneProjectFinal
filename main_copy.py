##### IMPORTS

import os
import asyncio
import logging
from dotenv import load_dotenv

# ADK Core Components
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

# Gemini/Vertex AI Types
from google.genai import types
from google.genai.types import GenerateContentConfig, Retrieval, VertexRagStore

# Vertex AI SDK (RAG corpus)
import vertexai
from google import genai
from vertexai import rag
from google.adk.plugins.logging_plugin import (
    LoggingPlugin,
)  # <---- 1. Import the Plugin

logging.basicConfig(level=logging.DEBUG) 

print("ADK components imported successfully.")

##########3

PROJECT_ID = "agents-capstone-project"

DOCUMENT = r"document.txt"

vertexai.init(project=PROJECT_ID, location="us-east1")
client = genai.Client(vertexai=True, project=PROJECT_ID, location="us")

try: 
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print("Google API Key Complete")
except KeyError: 
    print("Authentication Error: please create a .env file with 'GOOGLE_API_KEY")


# To handle failures like rate limits or temporary unavailability of the model, we can use a retry mechanism.
retry_configuration = types.HttpRetryOptions(
    attempts = 5,
    exp_base = 7,
    initial_delay = 1,
    http_status_codes = [429, 500, 502, 503, 504]
)


# Currently supports Google first-party embedding models
# fmt: off
EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"  # @param {type:"string", isTemplate: true}
# fmt: on

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
    path=r"rubrics.pdf",
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


print("RAG tool created successfully.")
###############################################################
config_with_rag = GenerateContentConfig(
    tools=[rag_retrieval_tool] # Retrieval Object injected here
)

# Parallel reviewers

# Agent focused on presentation
# "You are a 'Criteria A' Presentation reviewer. Your task is to review the presentation and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation.".strip()
# Definición del prompt largo (sin la asignación directa que puede causar error)
PRESENTATION_PROMPT = "You are a 'Criterion A' Presentation reviewer. Your task is to review the document according to rubric of criterion A and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation."
presentation_reviewer = Agent(
    name = "PresentationReviewer",
    model=Gemini(model_name = "gemini-2.5-flash-lite", config = config_with_rag),
    tools=[],
    instruction = PRESENTATION_PROMPT,
    output_key = "Presentation_feedback",
    )

print("Presentation reviewer created successfully.")


MATH_COM_PROMPT = "You are a 'Criterion B' Mathematical Communication reviewer. Your task is to review the document according to rubric of criterion B and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation."
math_com_reviewer = Agent(
    name = "MathComReviewer",
    model=Gemini(model_name = "gemini-2.5-flash-lite", config = config_with_rag),
    tools=[],
    instruction = MATH_COM_PROMPT,
    output_key = "Mathematical_communication_feedback",
    )

print("Mathematical Communication reviewer created successfully.")

PERS_ENG_PROMPT = "You are a 'Criterion C' Personal Engagement reviewer. Your task is to review the document according to rubric of criterion C and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation."
pers_eng_reviewer = Agent(
    name = "PersEngReviewer",
    model=Gemini(model_name = "gemini-2.5-flash-lite", config = config_with_rag),
    tools=[],
    instruction = PERS_ENG_PROMPT,
    output_key = "Personal_engagement_feedback",
    )

print("Personal Engagement reviewer created successfully.")


REFLECTION_PROMPT = "You are a 'Criterion D' Reflection reviewer. Your task is to review the document according to rubric of criterion D and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation."
reflection_reviewer = Agent(
    name = "ReflectionReviewer",
    model=Gemini(model_name = "gemini-2.5-flash-lite", config = config_with_rag),
    tools=[],
    instruction = REFLECTION_PROMPT,
    output_key = "Reflection_feedback",
    )

print("Reflection reviewer created successfully.")

USE_MATH_PROMPT = "You are a 'Criterion E' Use of Mathematics reviewer. Your task is to review the document according to rubric of criterion E and provide feedback. You must provide a score according to the rubric and justify your score. You must also provide 3 actionables that the student can take to improve their document presentation."
use_math_reviewer = Agent(
    name = "UseMathReviewer",
    model=Gemini(model_name = "gemini-2.5-flash-lite", config = config_with_rag),
    tools=[],
    instruction = USE_MATH_PROMPT,
    output_key = "Use_of_Mathematics_feedback",
    )

print("Use of Mathematics reviewer created successfully.")

aggregator_agent = Agent(
    name = "AggregatorAgent",
    model = Gemini(model_name = "gemini-2.5-flash-lite", retry_options = retry_configuration),
    instruction="""Combine these five feedbacks into a single final report:

    **Presentation feedback:**
    ${Presentation_feedback}
    
    *Mathematical Communication feedback:**
    ${Mathematical_communication_feedback}
    
    **Personal Engagement feedback:**
    ${Personal_engagement_feedback}

    **Reflection feedback:**
    ${Reflection_feedback}

    **Use of Mathematics feedback**
    ${Use_of_Mathematics_feedback}
    
    Your summary should highlight common themes, surprising connections, and the most important key takeaways from all five feedbacks. The final summary should be around 200 words.""",
    output_key="final_feedback",  # This will be the final output of the entire system.
)

print("Aggregator_agent created.")


# The ParallelAgent runs all its sub-agents simultaneously.
parallel_feedback_team = ParallelAgent(
    name="SequentialFeedbackTeam",
    sub_agents=[presentation_reviewer, math_com_reviewer, pers_eng_reviewer, reflection_reviewer, use_math_reviewer],
)

# This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
root_agent = SequentialAgent(
    name="FeedbackSystem",
    sub_agents=[parallel_feedback_team, aggregator_agent],
)

print("Parallel and Sequential Agents created.")

########################

# -----------------AGENTS FLOW EXECUTION -----------------

#Asynchronous function for runner
async def run_feedback_system():
    # Runner definition
    runner = InMemoryRunner(agent=root_agent,
    plugins=[
        LoggingPlugin()
    ],  # <---- 2. Add the)
    )
    
    # Define input text (document to be analyzed)
    try:
        with open(DOCUMENT, 'r', encoding='utf-8') as f:
            TEXT_FOR_REVIEW = f.read()
    except FileNotFoundError:
        TEXT_FOR_REVIEW = "Error: Input document not found. Please simulate the review using the prompt description."
        
    
    TASK_PROMPT = f"""
    {TEXT_FOR_REVIEW}

    ---
    **TASK:** Generate the final feedback report based on Criteria A, B, C, D, and E, reviewing the document provided above.
    """
    
    print(f"\n--- Starting Workflow: {root_agent.name} ---")
    print(f"Input task: {TASK_PROMPT[:100]}...") 

    response = await runner.run_debug(
        TASK_PROMPT
    )
    print("******RESPONSE*******\n", response, "******RESPONSE*******\n")
    # Extract final_feedback values from elements where state_delta contains 'final_feedback'
    final_feedback_values = []
    for event in response:
        if (hasattr(event, 'actions') and 
            event.actions is not None and 
            hasattr(event.actions, 'state_delta') and 
            event.actions.state_delta is not None and 
            isinstance(event.actions.state_delta, dict) and 
            'final_feedback' in event.actions.state_delta):
            final_feedback_values.append(event.actions.state_delta['final_feedback'])

    print("Final report: ", final_feedback_values)
    # Print the extracted values
    print("Extracted final_feedback values:")
    for i, value in enumerate(final_feedback_values, 1):
        print(f"\n--- Final Feedback {i} ---")
        print(value)

#------------------------------------------------------------
# CREATING CONSOLIDATED FEEDBACK
    
    consolidated_filename = "COMPLETE_FEEDBACK_REPORT.md"
    
    # Open file
    with open(consolidated_filename, "w", encoding="utf-8") as f:
        f.write("Consolidated feedback report\n\n")
        f.write("---")
        
        f.write("\n## I. Detailed feedback per criteria\n\n")
        f.write(final_feedback_values[0])
        """
        feedback_keys = [
            "Presentation_feedback",
            "Mathematical_communication_feedback",
            "Personal_engagement_feedback",
            "Reflection_feedback",
            "Use_of_Mathematics_feedback",
        ]
        
        key_to_title = {
            "Presentation_feedback": "A. Presentation",
            "Mathematical_communication_feedback": "B. Mathematical communication",
            "Personal_engagement_feedback": "C. Personal Engagement",
            "Reflection_feedback": "D. Reflection",
            "Use_of_Mathematics_feedback": "E. Use of Mathematics",
        }

        for key in feedback_keys:
            if key in all_outputs:
                f.write(f"### Criteria {key_to_title[key]}\n\n")
                f.write(all_outputs[key].strip())
                f.write("\n\n---\n") # Separador entre criterios
            else:
                f.write(f"### Criteria {key_to_title[key]} (not found)\n\n")

        # 2. WRITE FINAL REPORT (AggregatorAgent)
        f.write("\n## ✨ II. Final consolidated feedback\n\n")
        f.write(final_report_text.strip())
        f.write("\n")
        """
    # -----------------------------------------------
    # MOSTRAR Y CONFIRMAR
    print(f"\n--- Final Feedback (Aggregator Agent) ---")
    #print(final_report_text) 
    print(f"\n Complete report (individual and consolidated) saved in {consolidated_filename}")



# ----------------- PUNTO DE ENTRADA SÍNCRONO -----------------
if __name__ == "__main__":
    try:
        # Esto ejecuta la función asíncrona
        asyncio.run(run_feedback_system())
    except NameError:
        print("Error: Ensure that all variables (root_agent) are defined globally.")
    except Exception as e:
        print(f"A general error ocurred: {e}")