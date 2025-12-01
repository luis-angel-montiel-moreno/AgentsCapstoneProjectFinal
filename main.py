##### IMPORTS
"""
This script implements the "Solution" described in the Readme:
An agentic system that helps professors to review students' work automatically.
It addresses the "Problem" of time-consuming reviews by providing automated feedback,
scores, and actionables ("Value").

Main Entry Point:
This is the main orchestration script that initializes and executes the agentic
feedback system. It coordinates the workflow from document input to final report generation.

The system supports both PDF and text file formats for student documents:
- PDF files: Enables analysis of mathematical formulas, diagrams, and images
- Text files: Supports plain text documents with UTF-8 encoding
"""
import os
import asyncio
import logging
from dotenv import load_dotenv

from google.adk.runners import InMemoryRunner
from google.genai import types
from google.adk.plugins.logging_plugin import LoggingPlugin
from t_lib.t_agentic_lib.t_agent_controller import ReviewerAgentController
from t_lib.t_agentic_lib.t_inductive_agent_model.t_reviewer_agent_inductive import InductiveReviewerAgents
from t_lib.t_project.t_config import ProjectConfig

# Configure logging level for debugging and monitoring agent execution
logging.basicConfig(level=logging.DEBUG)

# ----------------- CONFIGURATION AND INITIALIZATION -----------------

# Load environment variables from .env file for API authentication
try: 
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print("Google API Key Complete")
except KeyError: 
    print("Authentication Error: please create a .env file with 'GOOGLE_API_KEY")

###############################################################
# Initialize the root agent system
# This sets up the entire agent hierarchy: parallel reviewers -> aggregator
ReviewerAgentController.set_root_reviewer_system_agent()
root_agent = ReviewerAgentController.root_reviewer_system_agent
########################

# ----------------- AGENTS FLOW EXECUTION -----------------

async def run_feedback_system():
    """
    Asynchronous function that orchestrates the entire feedback generation workflow.
    
    Workflow:
    1. Creates an InMemoryRunner with the root agent and logging plugin
    2. Loads the student document to be reviewed (supports PDF and text formats)
    3. Constructs the task prompt for the agent system
    4. Executes the agent workflow (parallel reviewers -> aggregator)
    5. Extracts feedback from all agents
    6. Writes consolidated feedback report to output file
    
    Document Format Support:
    - PDF files: Enables analysis of mathematical formulas, diagrams, and images
    - Text files: Supports plain text documents with UTF-8 encoding
    
    Returns:
        None (writes output to file)
    """
    # Initialize the agent runner with logging for debugging and monitoring
    # Initialize the agent runner with logging for debugging and monitoring
    # app_name="agents" is required to match the default app name expected by the agents library
    runner = InMemoryRunner(
        agent=root_agent,
        app_name="agents",
        plugins=[
            LoggingPlugin()  # Enables detailed logging of agent execution
        ],  
    )
    
    # Create a session for the interaction
    session_id = "feedback_session"
    user_id = "user"
    await runner.session_service.create_session(
        session_id=session_id,
        user_id=user_id,
        app_name="agents"
    )
    
    # Construct the task prompt that will be sent to the agent system
    # This prompt instructs the system to generate feedback based on all rubric criteria
    TASK_INSTRUCTION = """
    **TASK:** Generate the final feedback report based on Criteria A, B, C, D, and E, reviewing the document provided above.
    """
    
    try:
        file_path = ProjectConfig.input_sample_document_to_review
        file_extension = os.path.splitext(file_path)[1].lower()
        
        parts = []
        
        if file_extension == '.pdf':
            # PDF format enables analysis of mathematical formulas, diagrams, and images
            # This is particularly valuable for thesis documents with complex mathematical content
            with open(file_path, "rb") as f:
                pdf_data = f.read()
            pdf_part = types.Part.from_bytes(data=pdf_data, mime_type="application/pdf")
            parts.append(pdf_part)
            print(f"Loaded PDF file: {file_path}")
        else:
            # Default to text file reading for plain text documents
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            parts.append(types.Part(text=text_content))
            print(f"Loaded text file: {file_path}")
            
        parts.append(types.Part(text=TASK_INSTRUCTION))
        
        input_content = types.Content(parts=parts, role="user")
        
    except FileNotFoundError:
        print("Error: Input document not found.")
        return
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return
    
    print(f"\n--- Starting Workflow: {root_agent.name} ---")

    # Execute the agent workflow and capture all response events
    response = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=input_content
    ):
        response.append(event)
        
    print("******RESPONSE RECEIVED*******\n")

    def get_output_key_response_value(output_key, response, output_title):
        """
        Helper function to extract output values from agent response events.
        
        This function searches through all response events to find the state_delta
        containing the specified output_key. This is used to extract feedback
        from each agent's output.
        
        Args:
            output_key (str): The key identifier for the desired output (e.g., 'presentation_feedback')
            response: The response object containing agent execution events
            
        Returns:
            str: The extracted value if found, empty string otherwise
        """
        for event in response:
            if (hasattr(event, 'actions') and
                    event.actions is not None and
                    hasattr(event.actions, 'state_delta') and
                    event.actions.state_delta is not None and
                    isinstance(event.actions.state_delta, dict) and
                    output_key in event.actions.state_delta):
                return "# " + output_title + "\n\n"+   event.actions.state_delta[output_key]
        return ""

    # Extract feedback from all individual reviewer agents
    # Each agent provides feedback for one rubric criterion (A, B, C, D, or E)
    final_feedback_values = []
    for agent in InductiveReviewerAgents.reviewer_agents:
        final_feedback_values.append(get_output_key_response_value(agent.output_key, response, agent.output_title))

    # Extract the final consolidated feedback from the aggregator agent
    final_feedback_values.append(get_output_key_response_value('final_feedback', response, "Final Feedback"))

    print("Final report: ", final_feedback_values)
    # Display all extracted feedback values for verification
    print("Extracted final_feedback values:")
    for i, value in enumerate(final_feedback_values, 1):
        print(f"\n--- Final Feedback {i} ---")
        print(value)

    # ----------------- CREATING CONSOLIDATED FEEDBACK -----------------
    # Delivers the "Value": "time saving solution... providing a final score and a summary final feedback report"
    
    # Write the consolidated feedback report to the output file
    # This creates a markdown file with all feedback organized by criteria
    with open(ProjectConfig.consolidated_filename, "w", encoding="utf-8") as f:
        f.write("# Consolidated feedback report\n\n")
        f.write("---")
        for feedback in final_feedback_values:
            f.write("\n")
            f.write(feedback)
            f.write("\n")
            f.write("---")
            f.write("\n")

    # Display completion message with output file location
    print(f"\n Complete report (individual and consolidated) saved in {ProjectConfig.consolidated_filename}")


# ----------------- SYNCHRONOUS ENTRY POINT -----------------
if __name__ == "__main__":
    """
    Main entry point for the script.
    Executes the asynchronous feedback system workflow.
    """
    try:
        # Execute the asynchronous function using asyncio
        asyncio.run(run_feedback_system())
    except NameError:
        print("Error: Ensure that all variables (root_agent) are defined globally.")
    except Exception as e:
        print(f"A general error ocurred: {e}")