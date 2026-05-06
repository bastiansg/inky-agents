FROM inky-agents-core

COPY src/inky_agents /src/src/inky_agents
COPY requirements.txt pyproject.toml /src/
RUN --mount=type=bind,target=/root/.cache,source=.git,target=/src/.git \
    uv pip install /src --no-deps

WORKDIR /src
CMD python -m inky_agents.app.app
