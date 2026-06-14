"""Command-line interface for the application."""

from __future__ import annotations

import sys

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.utils.content_utils import extract_text_from_content
from google.genai import types

from greeting_card_writer.birthday_writer import create_birthday_writer
from greeting_card_writer.get_well_writer import create_get_well_writer
from greeting_card_writer.sympathy_writer import create_sympathy_writer


async def main(argv: list[str] | None = None) -> None:
    """Run the command-line interface."""
    prompt = " ".join(sys.argv[1:])
    if not prompt:
        example = "Congratulate Jenny on her high school graduation, from Fred."
        raise SystemExit(f'Usage: python -m greeting_card_writer "{example}"')

    app_name = "greeting_card_writer"
    user_id = "cli_user"
    session_id = "cli_session"

    birthday_writer = create_birthday_writer()
    if not birthday_writer:
        raise RuntimeError("Could not create a birthdy writer.")

    get_well_writer = create_get_well_writer()
    if not get_well_writer:
        raise RuntimeError("Could not create a get well_ writer.")

    sympathy_writer = create_sympathy_writer()
    if not sympathy_writer:
        raise RuntimeError("Could not create a sympathy writer")

    agent = Agent(
        name="greeting_card_writer",
        description=(
            "The main coordinator agents. "
            "Handles the user's request and delegates the writing to specialist agents."
        ),
        instruction=(
            "Review the user's request for a greeting card, "
            "and assign the task to a sub-agent. "
            "If the user has requested a birthday card, "
            "delegate to the `birthday_writer`. "
            "If the user has requested a get well card, "
            "delegate to the `get_well_writer`. "
            "If the user has requested a sympathy card, "
            "delegate to the `sympathy_writer`. "
            "If the user's request cannot be delegated to a specialist sub-agent, "
            "reply that you are unable to help with the request."
        ),
        sub_agents=[birthday_writer, get_well_writer, sympathy_writer],
    )

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            final_text = extract_text_from_content(event.content)

    print(final_text)
