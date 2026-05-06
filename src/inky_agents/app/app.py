import os
import logfire
import asyncio

from rich.console import Console

from inky_dsp.pipelines import display_image
from inky_dsp.buttons import InkyButtons, ButtonMap, ButtonEvent

from inky_agents.pipelines import other_presents_pipline


if os.getenv("LOGFIRE_TOKEN") is not None:
    logfire.configure(service_name="inky_agents")
    logfire.instrument_pydantic_ai()
    logfire.instrument_openai()


console = Console()


async def on_button_pressed(event: ButtonEvent) -> None:
    if event.label == "A":
        await other_presents_pipline()


async def main() -> None:
    buttons = InkyButtons(
        button_map=ButtonMap(),
        callback=on_button_pressed,
    )

    await buttons.run()


if __name__ == "__main__":
    asyncio.run(main())
