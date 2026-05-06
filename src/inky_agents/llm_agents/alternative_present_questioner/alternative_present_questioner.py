from pathlib import Path

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_extra_types.language_code import LanguageName
from pydantic import BaseModel, Field, StrictInt, StrictStr
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent
from llm_agents.message_history import MongoDBMessageHistory


class AlternativePresentQuestionerDeps(BaseModel):
    n: StrictInt = Field(
        default=5,
        description="The number of alternative-present questions to generate.",
        ge=1,
    )

    output_language: LanguageName = Field(
        default="Spanish",
        description="The language to use for the generated questions.",
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
    deps_type=AlternativePresentQuestionerDeps,
    output_type=NativeOutput(AlternativePresentQuestionerOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(
    ctx: RunContext[AlternativePresentQuestionerDeps],
) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class AlternativePresentQuestioner(
    LLMAgent[
        AlternativePresentQuestionerDeps, AlternativePresentQuestionerOutput
    ]
):
    def __init__(
        self,
        mongodb_message_history: MongoDBMessageHistory,
        max_concurrency: int = 10,
    ):
        super().__init__(
            agent=agent,
            max_concurrency=max_concurrency,
            mongodb_message_history=mongodb_message_history,
        )
