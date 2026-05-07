import io
import os
import cairosvg
import replicate

from PIL import Image
from uuid import uuid4
from datetime import date

from functools import lru_cache
from rich.console import Console

from inky_dsp.pipelines import display_image
from llm_agents.message_history import MongoDBMessageHistory

from inky_agents.config import config
from inky_agents.llm_agents import (
    PresentQuestioner,
    PresentQuestionerDeps,
    ImagePrompter,
    ImagePrompterDeps,
)


console = Console()


OUT_PATH = "/resources/images/present-questioner"
os.makedirs(OUT_PATH, exist_ok=True)


@lru_cache()
def get_present_questioner() -> PresentQuestioner:
    return PresentQuestioner(
        mongodb_message_history=MongoDBMessageHistory(
            session_id="0",
            mongodb_dsn=config.mongodb_dsn,
            message_limit=10,
        )
    )


@lru_cache()
def get_image_prompter() -> ImagePrompter:
    return ImagePrompter()


async def other_presents_pipline():

    pq = get_present_questioner()
    pq_output = await pq.generate(
        user_prompt="Provide your wildly creative question about alternative presents.",
        agent_deps=PresentQuestionerDeps(
            output_language="Spanish",
        ),
    )

    question = pq_output.question
    console.print(question)

    ip = get_image_prompter()
    ip_output = await ip.generate(
        user_prompt="Provide your surreal image-generation prompt.",
        agent_deps=ImagePrompterDeps(question=question),
    )

    image_generation_prompt = ip_output.flux_prompt
    rep_output = replicate.run(
        "recraft-ai/recraft-v4-svg",
        input={
            "prompt": image_generation_prompt,
            "size": "832x1280",
        },
    )

    svg_bytes = rep_output.read()
    png_bytes = cairosvg.svg2png(bytestring=svg_bytes)
    image = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    gen_image_path = f"{OUT_PATH}/{date.today().isoformat()}-{uuid4()}.jpg"
    image.save(gen_image_path)

    display_image(file_path=gen_image_path)
