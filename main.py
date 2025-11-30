##### IMPORTS
"""
This script implements the "Solution" described in the Readme:
An agentic system that helps professors to review students' work automatically.
It addresses the "Problem" of time-consuming reviews by providing automated feedback,
scores, and actionables ("Value").
"""
import os
import asyncio
import logging
from dotenv import load_dotenv

from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.plugins.logging_plugin import LoggingPlugin
from t_lib.t_agentic_lib.t_agent_controller import ReviewerAgentController
from t_lib.t_project.t_config import ProjectConfig

logging.basicConfig(level=logging.DEBUG)

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


###############################################################
ReviewerAgentController.set_root_reviewer_system_agent()
root_agent = ReviewerAgentController.root_reviewer_system_agent
########################

# -----------------AGENTS FLOW EXECUTION -----------------

#Asynchronous function for runner
async def run_feedback_system():
    # Runner definition
    runner = InMemoryRunner(agent=root_agent,
    plugins=[
        LoggingPlugin()
    ],  
    )
    
    # Define input text (document to be analyzed)
    try:
        with open(ProjectConfig.input_sample_document_to_review, 'r', encoding='utf-8') as f:
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
    # Delivers the "Value": "time saving solution... providing a final score and a summary final feedback report"

    
    # Open file
    with open(ProjectConfig.consolidated_filename, "w", encoding="utf-8") as f:
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
    print(f"\n Complete report (individual and consolidated) saved in {ProjectConfig.consolidated_filename}")



# ----------------- PUNTO DE ENTRADA SÍNCRONO -----------------
if __name__ == "__main__":
    try:
        # Esto ejecuta la función asíncrona
        asyncio.run(run_feedback_system())
    except NameError:
        print("Error: Ensure that all variables (root_agent) are defined globally.")
    except Exception as e:
        print(f"A general error ocurred: {e}")