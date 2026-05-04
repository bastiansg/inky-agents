from pathlib import Path

from pydantic import BaseModel, Field, StrictInt, StrictStr
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent


class AlternativePresentQuestionerDeps(BaseModel):
    n: StrictInt = Field(
        default=10,
        description="The number of alternative-present questions to generate.",
        ge=1,
    )


class AlternativePresentQuestionerOutput(BaseModel):
    questions: list[StrictStr] = Field(
        description="Wildly creative questions about alternative presents.",
        min_length=1,
    )


agent = Agent(  # type: ignore
    name="alternative-present-questioner",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=AlternativePresentQuestionerDeps,
    output_type=AlternativePresentQuestionerOutput,
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class AlternativePresentQuestioner(
    LLMAgent[
        AlternativePresentQuestionerDeps, AlternativePresentQuestionerOutput
    ]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
