"""
Base Agent Model Module

This module defines the base class for all reviewer agents in the system.
It implements a template pattern where each agent follows the same structure
but specializes in reviewing a specific rubric criterion.

Design Pattern:
This uses inheritance to create specialized agents from a common base class,
ensuring consistency in agent behavior while allowing specialization per criterion.
"""

from typing import ClassVar
from google.adk.agents import Agent

# Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
class ReviewerAgent(Agent):
    """
    Base class for all individual reviewer agents.
    
    This class defines the common structure and behavior for agents that review
    student documents according to specific rubric criteria. Each instance of this
    class is specialized to review one criterion (A, B, C, D, or E).
    
    Responsibilities:
    - Review document according to assigned rubric criterion
    - Provide a numerical score based on rubric standards
    - Justify the assigned score with specific feedback
    - Generate 3 actionable recommendations for improvement
    
    Attributes:
        GOAL_PROMPT (ClassVar[str]): Template string for agent instruction prompt
        role (str): Descriptive role of the agent (e.g., "Criterion A Presentation reviewer")
        role_letter (str): Letter identifier for the rubric criterion (A, B, C, D, or E)
        output_title (str): Title for this agent's output section in the final report
        output_key (str): Unique key identifier for extracting this agent's feedback
    
    Architecture:
    This class implements the Template Method pattern, where the base class
    defines the structure (instruction format, output handling) and subclasses
    or instances provide the specific details (criterion, role, etc.).
    """
    # Template instruction prompt that gets formatted with specific role and criterion
    GOAL_PROMPT: ClassVar[str] = (
        f"You are a {0}. "
        f"Your task is to review the document according to rubric of criterion {1} and provide feedback. "
        f"You must provide a score according to the rubric and justify your score. "
        f"You must also provide 3 actionable that the student can take to improve their document presentation."
    )
    role: str
    role_letter: str
    output_title: str

    def __init__(self, role, role_letter, name, model, tools, output_key, output_title):
        """
        Initialize a ReviewerAgent instance.
        
        Creates a specialized agent for reviewing a specific rubric criterion.
        The agent is configured with a formatted instruction prompt and assigned
        a unique output key for result extraction.
        
        Args:
            role (str): Descriptive role name for the agent
            role_letter (str): Criterion letter (A, B, C, D, or E)
            name (str): Unique agent identifier
            model: LLM model instance to use for this agent (typically Gemini)
            tools (list): List of tools available to the agent (includes RAG tool)
            output_key (str): Unique key for extracting this agent's feedback from response
            output_title (str): Display title for this agent's feedback section
        """
        super().__init__(
            name=name,
            model=model,
            tools=[],  # Tools are passed but empty list used - consider using tools parameter
            instruction=self.GOAL_PROMPT.format(role, role_letter),
            output_key=output_key,
            role=role,
            role_letter=role_letter,
            output_title=output_title,
        )
        print(f"{self.name} agent created successfully.")








