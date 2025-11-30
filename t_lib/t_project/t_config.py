"""
Configuration module for the Agents Capstone Project.

This module centralizes all configuration settings including file paths,
project identifiers, and other constants used throughout the application.
Centralizing configuration makes it easier to maintain and modify paths
without changing code in multiple files.
"""

class ProjectConfig:
    """
    Central configuration class containing all project settings.
    
    This class stores:
    - Project identifiers for Google Cloud services
    - Input file paths (student documents, rubrics)
    - Output file paths (generated feedback reports)
    
    Attributes:
        project_id (str): Google Cloud project ID for Vertex AI services
        input_sample_document_to_review (str): Path to the student document to be reviewed
        input_rubrics_file (str): Path to the PDF file containing rubric criteria
        consolidated_filename (str): Path where the final consolidated feedback report will be saved
    """
    # Google Cloud project identifier for Vertex AI and RAG services
    project_id = "agents-capstone-project"
    
    # Path to the student document that will be reviewed by the agentic system
    input_sample_document_to_review = r"./resources/input/document.txt"
    
    # Path to the rubric PDF file that will be ingested into the RAG corpus
    # This rubric defines the criteria (A, B, C, D, E) used for evaluation
    input_rubrics_file = r"./resources/input/rubrics.pdf" 
    
    # Output file path where the consolidated feedback report will be written
    consolidated_filename = "./resources/output/COMPLETE_FEEDBACK_REPORT.md"

