from rich.console import Console

from inky_agents.config import config
from llm_agents.message_history import MongoDBMessageHistory
from inky_agents.llm_agents import (
    AlternativePresentQuestioner,
    AlternativePresentQuestionerDeps,
)


console = Console()


async def other_presents_pipline():
    apq = AlternativePresentQuestioner(
        mongodb_message_history=MongoDBMessageHistory(
            session_id="0",
            mongodb_dsn=config.mongodb_dsn,
        )
    )

    apq_output = await apq.generate(
        user_prompt="Wildly creative questions about alternative presents.",
        agent_deps=AlternativePresentQuestionerDeps(
            n=5,
            output_language="Spanish",
        ),
    )

    console.print(apq_output)
