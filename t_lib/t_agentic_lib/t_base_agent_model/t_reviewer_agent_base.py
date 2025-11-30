from typing import ClassVar
from google.adk.agents import Agent

# Part of the "Solution": "uses agentic AI to provide a feedback to the professor"
class ReviewerAgent(Agent):
    GOAL_PROMPT: ClassVar[str] = (f"You are a {0}. "
                   f"Your task is to review the document according to rubric of criterion {1} and provide feedback. "
                   f"You must provide a score according to the rubric and justify your score. "
                   f"You must also provide 3 actionable that the student can take to improve their document presentation.")
    role: str
    role_letter: str
    output_title: str

    def __init__(self, role, role_letter, name, model, tools, output_key, output_title):
        super().__init__(
            name= name,
            model= model,
            tools=[],
            instruction= self.GOAL_PROMPT.format(role, role_letter),
            output_key= output_key,
            role= role,
            role_letter= role_letter,
            output_title= output_title,
        )
        print(f"{self.name} agent created successfully.")








