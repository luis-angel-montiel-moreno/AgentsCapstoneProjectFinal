from google.adk.agents import Agent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from t_lib.t_agentic_lib.t_base_agent_model.t_reviewer_agent_base import ReviewerAgent
import os

class InductiveReviewerAgents:
    reviewer_agents = []
    parallel_feedback_team_agent = None
    parallel_reviewers_aggregator_agent = None

    # Parallel reviewers
    # Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
    # Each agent focuses on one criterion of the rubric to provide detailed, specific feedback.
    @staticmethod
    def init_reviewer_agents(rag_tool):

        # To handle failures like rate limits or temporary unavailability of the model, we can use a retry mechanism.
        retry_configuration = types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 502, 503, 504]
        )

        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"DEBUG: API Key present: {bool(api_key)}")
        model_agent_reviewer = Gemini(model = "gemini-2.5-flash-lite", retry_options = retry_configuration, api_key=api_key)

        # A list of parameters for the agents
        # Each agent will be focused on one criterion of the rubric
        # role, role_letter, name, output_key, output_title
        parameters = [
            ["'Criterion A' Presentation reviewer", "A", "PresentationReviewerAgent", "presentation_feedback", "Presentation feedback"],
            ["'Criterion B' Mathematical Communication reviewer", "B", "MathComReviewerAgent", "mathematical_communication_feedback", "Mathematical communication feedback"],
            ["'Criterion C' Personal Engagement reviewer", "C", "PersEngReviewerAgent", "personal_engagement_feedback", "Personal engagement feedback"],
            ["'Criterion D' Reflection reviewer", "D", "ReflectionReviewerAgent", "reflection_feedback", "Reflection feedback"],
            ["'Criterion E' Use of Mathematics reviewer", "E", "UseMathReviewerAgent", "use_of_Mathematics_feedback", "Use of Mathematics feedback"],
        ]
        reviewer_agents = []
        for role, role_letter, name, output_key, output_title in parameters:
            reviewer_agents.append(
                ReviewerAgent(role = role,
                              role_letter = role_letter,
                              name = name,
                              model = model_agent_reviewer,
                              tools = [rag_tool],
                              output_key = output_key,
                              output_title= output_title)
            )
        return reviewer_agents


    # Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
    # Each agent focuses on one criterion of the rubric to provide detailed, specific feedback.
    @staticmethod
    def set_reviewers_agents(rag_retrieval_tool):
        InductiveReviewerAgents.reviewer_agents = InductiveReviewerAgents.init_reviewer_agents(rag_tool = rag_retrieval_tool)
        print("All reviewer agents initialized.")

    # Parallel reviewers
    # The ParallelAgent runs all its sub-agents simultaneously.
    @staticmethod
    def set_parallel_feedback_team_agent():
        parallel_feedback_team_agent = ParallelAgent(
            name="ParallelFeedbackTeamAgent",
            sub_agents=InductiveReviewerAgents.reviewer_agents,
        )
        InductiveReviewerAgents.parallel_feedback_team_agent = parallel_feedback_team_agent
        print("All parallel reviewer agents initialized.")

    # Aggregator Agent Reviewers
    # Part of the "Solution": "provides a final score based on the rubric criteria and a summary final feedback report"
    # Consolidates individual agent feedback into a cohesive report.
    @staticmethod
    def set_parallel_reviewers_aggregator_agent():
        # To handle failures like rate limits or temporary unavailability of the model, we can use a retry mechanism.
        retry_configuration = types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 502, 503, 504]
        )

        partial_aggregator_instruction = ""
        for agent in InductiveReviewerAgents.reviewer_agents:
            partial_aggregator_instruction += f"**${agent.output_title}:**\n\n${agent.output_key}\n\n"

        InductiveReviewerAgents.parallel_reviewers_aggregator_agent = Agent(
            name="ParallelReviewersAggregatorAgent",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_configuration, api_key=os.getenv("GOOGLE_API_KEY")),
            instruction=f"Combine these following feedbacks into a single final report:\n {partial_aggregator_instruction} \n"
                        f"Your summary should highlight common themes, surprising connections, and the most important key takeaways from all five feedbacks."
                        f"The final summary should be around 200 words.",
            output_key="final_feedback",  # This will be the final output of the entire system.
        )
        print("Parallel aggregator reviewer agent initialized.")
