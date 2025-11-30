"""
Agent Controller Module

This module serves as the main orchestrator for the entire agentic feedback system.
It coordinates the initialization and composition of all agents into a hierarchical
workflow that processes student documents through parallel review and aggregation.

Architecture Role:
The controller pattern is used here to centralize agent initialization and
composition logic, making the system easier to understand and modify.
"""

from google.adk.agents import SequentialAgent
from t_lib.t_agentic_lib.t_inductive_agent_model.t_reviewer_agent_inductive import InductiveReviewerAgents
from t_lib.t_agentic_lib.t_agent_rag.t_retrieval_rag_tool import RetrievalRagTool

class ReviewerAgentController:
    """
    Controller class that manages the initialization and composition of the agentic system.
    
    This class implements the orchestration logic for the entire feedback workflow:
    1. Initialize RAG tool for rubric retrieval
    2. Create individual reviewer agents for each rubric criterion
    3. Compose agents into parallel execution team
    4. Create aggregator agent for final report generation
    5. Combine everything into a sequential workflow
    
    The root agent follows a SequentialAgent pattern:
    Step 1: Parallel execution of all reviewer agents (Criteria A-E)
    Step 2: Aggregation of all feedback into final report
    
    Attributes:
        root_reviewer_system_agent (SequentialAgent): The top-level agent that orchestrates
            the entire feedback generation workflow
    """
    root_reviewer_system_agent = None

    @staticmethod
    def set_root_reviewer_system_agent():
        """
        Initializes and composes the complete agentic feedback system.
        
        This method sets up the entire agent hierarchy:
        - Creates RAG retrieval tool for rubric access
        - Initializes individual reviewer agents (one per rubric criterion)
        - Groups reviewers into a parallel execution team
        - Creates an aggregator agent to synthesize feedback
        - Composes everything into a sequential workflow
        
        Workflow Structure:
        SequentialAgent (FeedbackSystem)
        ├── ParallelAgent (ParallelFeedbackTeamAgent)
        │   ├── PresentationReviewerAgent (Criterion A)
        │   ├── MathComReviewerAgent (Criterion B)
        │   ├── PersEngReviewerAgent (Criterion C)
        │   ├── ReflectionReviewerAgent (Criterion D)
        │   └── UseMathReviewerAgent (Criterion E)
        └── Agent (ParallelReviewersAggregatorAgent)
        
        Part of the "Solution": Uses agentic AI to provide feedback to professors
        by parallelizing rubric-based reviews and aggregating results.
        """
        # Step 1: Initialize RAG tool for rubric retrieval
        # This tool allows agents to access rubric criteria from the ingested PDF
        rag_retrieval_tool = RetrievalRagTool.get_retrieval_rag_tool()

        # Step 2: Initialize individual reviewer agents
        # Each agent focuses on one rubric criterion (A, B, C, D, or E)
        # Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
        # Each agent provides detailed, specific feedback for its assigned criterion
        InductiveReviewerAgents.set_reviewers_agents(rag_retrieval_tool=rag_retrieval_tool)

        # Step 3: Create parallel execution team
        # The ParallelAgent runs all reviewer agents simultaneously for efficiency
        InductiveReviewerAgents.set_parallel_feedback_team_agent()

        # Step 4: Create aggregator agent
        # Part of the "Solution": "provides a final score based on the rubric criteria 
        # and a summary final feedback report"
        # This agent consolidates individual agent feedback into a cohesive final report
        InductiveReviewerAgents.set_parallel_reviewers_aggregator_agent()

        # Step 5: Compose the root sequential agent
        # This SequentialAgent defines the high-level workflow:
        # First: Execute parallel reviewer team
        # Then: Execute aggregator to synthesize results
        root_reviewer_system_agent = SequentialAgent(
            name="FeedbackSystem",
            sub_agents=[
                InductiveReviewerAgents.parallel_feedback_team_agent, 
                InductiveReviewerAgents.parallel_reviewers_aggregator_agent
            ],
        )
        ReviewerAgentController.root_reviewer_system_agent = root_reviewer_system_agent

        print("root_reviewer_system_agent created.")







