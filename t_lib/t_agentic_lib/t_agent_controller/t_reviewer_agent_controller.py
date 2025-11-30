from google.adk.agents import SequentialAgent
from t_lib.t_agentic_lib.t_inductive_agent_model.t_reviewer_agent_inductive import InductiveReviewerAgents
from t_lib.t_agentic_lib.t_agent_rag.t_retrieval_rag_tool import RetrievalRagTool

class ReviewerAgentController:
    root_reviewer_system_agent = None

    # This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
    @staticmethod
    def set_root_reviewer_system_agent():

        rag_retrieval_tool = RetrievalRagTool.get_retrieval_rag_tool()

        # Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
        # Each agent focuses on one criterion of the rubric to provide detailed, specific feedback.
        InductiveReviewerAgents.set_reviewers_agents(rag_retrieval_tool = rag_retrieval_tool)

        # Parallel reviewers
        # The ParallelAgent runs all its sub-agents simultaneously.
        InductiveReviewerAgents.set_parallel_feedback_team_agent()

        # Aggregator Agent Reviewers
        # Part of the "Solution": "provides a final score based on the rubric criteria and a summary final feedback report"
        # Consolidates individual agent feedback into a cohesive report.
        InductiveReviewerAgents.set_parallel_reviewers_aggregator_agent()

        # This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
        root_reviewer_system_agent = SequentialAgent(
            name="FeedbackSystem",
            sub_agents=[InductiveReviewerAgents.parallel_feedback_team_agent, InductiveReviewerAgents.parallel_reviewers_aggregator_agent],
        )
        ReviewerAgentController.root_reviewer_system_agent = root_reviewer_system_agent

        print("root_reviewer_system_agent created.")







