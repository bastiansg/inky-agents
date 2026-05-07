from pathlib import Path


from pydantic import BaseModel, Field, StrictStr
from pydantic_extra_types.language_code import LanguageName

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.capabilities import ReinjectSystemPrompt
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent
from llm_agents.message_history import MongoDBMessageHistory


class PresentQuestionerDeps(BaseModel):
    output_language: LanguageName = Field(
        default="Spanish",
        description="The language to use for the generated question.",
    )


class PresentQuestionerOutput(BaseModel):
    question: StrictStr = Field(
        description="A wildly creative question about alternative presents.",
    )


agent = Agent(
    name="PresentQuestioner",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    deps_type=PresentQuestionerDeps,
    output_type=NativeOutput(PresentQuestionerOutput),
    retries=10,
    capabilities=[ReinjectSystemPrompt()],
)


@agent.system_prompt
async def get_system_prompt(
    ctx: RunContext[PresentQuestionerDeps],
) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class PresentQuestioner(
    LLMAgent[PresentQuestionerDeps, PresentQuestionerOutput]
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
