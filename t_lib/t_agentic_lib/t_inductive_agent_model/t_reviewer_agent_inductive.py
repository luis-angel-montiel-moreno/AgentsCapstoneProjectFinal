"""
Inductive Agent Model Module

This module implements the factory and composition patterns for creating and organizing
reviewer agents. It manages the creation of individual agents, their grouping into
parallel execution teams, and the creation of an aggregator agent.

The term "inductive" refers to the approach of creating specialized agents and then
composing them into a higher-level system, building from specific to general.
"""

from google.adk.agents import Agent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from t_lib.t_agentic_lib.t_base_agent_model.t_reviewer_agent_base import ReviewerAgent
import os

class InductiveReviewerAgents:
    """
    Factory and composition class for creating and organizing reviewer agents.
    
    This class manages the lifecycle of all agents in the system:
    - Creates individual reviewer agents for each rubric criterion
    - Composes agents into parallel execution teams
    - Creates aggregator agent for final report synthesis
    
    Attributes:
        reviewer_agents (list): List of individual ReviewerAgent instances (one per criterion)
        parallel_feedback_team_agent (ParallelAgent): Agent that runs all reviewers in parallel
        parallel_reviewers_aggregator_agent (Agent): Agent that synthesizes all feedback into final report
    """
    reviewer_agents = []
    parallel_feedback_team_agent = None
    parallel_reviewers_aggregator_agent = None

    @staticmethod
    def init_reviewer_agents(rag_tool):
        """
        Factory method that creates all individual reviewer agent instances.
        
        This method initializes one ReviewerAgent for each rubric criterion (A-E).
        Each agent is configured with:
        - A specific role and criterion focus
        - Access to the RAG tool for rubric retrieval
        - A unique output key for result extraction
        - Retry configuration for reliability
        
        Args:
            rag_tool: The RAG retrieval tool that provides access to rubric criteria
            
        Returns:
            list: List of ReviewerAgent instances, one for each rubric criterion
            
        Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
        Each agent focuses on one criterion of the rubric to provide detailed, specific feedback.
        """
        # Configure retry mechanism for handling API failures
        # This improves system reliability by automatically retrying on rate limits
        # and temporary service unavailability
        retry_configuration = types.HttpRetryOptions(
            attempts=5,              # Maximum number of retry attempts
            exp_base=7,              # Exponential backoff base (7^attempt seconds)
            initial_delay=1,         # Initial delay before first retry (seconds)
            http_status_codes=[429, 500, 502, 503, 504]  # Status codes that trigger retry
        )

        # Retrieve API key from environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"DEBUG: API Key present: {bool(api_key)}")
        
        # Initialize Gemini model with retry configuration for all reviewer agents
        model_agent_reviewer = Gemini(
            model="gemini-2.5-flash-lite",
            retry_options=retry_configuration,
            api_key=api_key
        )

        # Agent configuration parameters
        # Each tuple defines: role description, criterion letter, agent name, output key, output title
        # This data-driven approach makes it easy to add or modify agents
        parameters = [
            ["'Criterion A' Presentation reviewer", "A", "PresentationReviewerAgent", "presentation_feedback", "Presentation feedback"],
            ["'Criterion B' Mathematical Communication reviewer", "B", "MathComReviewerAgent", "mathematical_communication_feedback", "Mathematical communication feedback"],
            ["'Criterion C' Personal Engagement reviewer", "C", "PersEngReviewerAgent", "personal_engagement_feedback", "Personal engagement feedback"],
            ["'Criterion D' Reflection reviewer", "D", "ReflectionReviewerAgent", "reflection_feedback", "Reflection feedback"],
            ["'Criterion E' Use of Mathematics reviewer", "E", "UseMathReviewerAgent", "use_of_Mathematics_feedback", "Use of Mathematics feedback"],
        ]
        
        # Create ReviewerAgent instance for each criterion
        reviewer_agents = []
        for role, role_letter, name, output_key, output_title in parameters:
            reviewer_agents.append(
                ReviewerAgent(
                    role=role,
                    role_letter=role_letter,
                    name=name,
                    model=model_agent_reviewer,
                    tools=[rag_tool],  # Each agent has access to RAG tool for rubric retrieval
                    output_key=output_key,
                    output_title=output_title
                )
            )
        return reviewer_agents

    @staticmethod
    def set_reviewers_agents(rag_retrieval_tool):
        """
        Initializes and stores all reviewer agents.
        
        This method creates all individual reviewer agents and stores them in
        the class variable for later use in parallel composition.
        
        Args:
            rag_retrieval_tool: The RAG tool providing rubric access to agents
            
        Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
        Each agent focuses on one criterion of the rubric to provide detailed, specific feedback.
        """
        InductiveReviewerAgents.reviewer_agents = InductiveReviewerAgents.init_reviewer_agents(rag_tool=rag_retrieval_tool)
        print("All reviewer agents initialized.")

    @staticmethod
    def set_parallel_feedback_team_agent():
        """
        Creates a ParallelAgent that runs all reviewer agents simultaneously.
        
        This method groups all individual reviewer agents into a parallel execution
        team. The ParallelAgent executes all sub-agents concurrently, significantly
        improving system performance by reducing total execution time.
        
        Performance Benefit:
        Instead of sequential execution (Agent A -> Agent B -> ... -> Agent E),
        all agents run in parallel, reducing total time from sum(times) to max(time).
        
        Architecture:
        The ParallelAgent pattern enables concurrent processing, which is ideal
        when agents are independent (each reviewing a different criterion).
        """
        parallel_feedback_team_agent = ParallelAgent(
            name="ParallelFeedbackTeamAgent",
            sub_agents=InductiveReviewerAgents.reviewer_agents,  # All 5 reviewer agents
        )
        InductiveReviewerAgents.parallel_feedback_team_agent = parallel_feedback_team_agent
        print("All parallel reviewer agents initialized.")

    @staticmethod
    def set_parallel_reviewers_aggregator_agent():
        """
        Creates an aggregator agent that synthesizes all reviewer feedback into a final report.
        
        This method creates a specialized agent that:
        - Takes input from all individual reviewer agents
        - Identifies common themes across all feedback
        - Highlights surprising connections between criteria
        - Generates a concise final summary report
        
        Part of the "Solution": "provides a final score based on the rubric criteria
        and a summary final feedback report"
        
        The aggregator consolidates individual agent feedback into a cohesive report,
        providing the professor with both detailed per-criterion feedback and an
        overall summary.
        
        Architecture:
        This agent dynamically constructs its instruction prompt based on all
        reviewer agents' output keys, making it adaptable to changes in agent configuration.
        """
        # Configure retry mechanism for aggregator agent as well
        retry_configuration = types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 502, 503, 504]
        )

        # Dynamically construct instruction prompt by referencing all reviewer agent outputs
        # This makes the aggregator automatically adapt to the reviewer agents' structure
        partial_aggregator_instruction = ""
        for agent in InductiveReviewerAgents.reviewer_agents:
            # Template variables ($output_title, $output_key) will be replaced at runtime
            # with actual feedback from each reviewer agent
            partial_aggregator_instruction += f"**${agent.output_title}:**\n\n${agent.output_key}\n\n"

        # Create the aggregator agent with dynamically constructed instruction
        InductiveReviewerAgents.parallel_reviewers_aggregator_agent = Agent(
            name="ParallelReviewersAggregatorAgent",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=retry_configuration,
                api_key=os.getenv("GOOGLE_API_KEY")
            ),
            instruction=(
                f"Combine these following feedbacks into a single final report:\n {partial_aggregator_instruction} \n"
                f"Your summary should highlight common themes, surprising connections, and the most important key takeaways from all five feedbacks. "
                f"The final summary should be around 200 words."
            ),
            output_key="final_feedback",  # This will be the final output of the entire system
        )
        print("Parallel aggregator reviewer agent initialized.")
