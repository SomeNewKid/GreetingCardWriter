from __future__ import annotations

from google.adk.agents import Agent


def create_get_well_writer() -> Agent | None:
    try:
        return Agent(
            name="get_well_writer",
            description='Writes a "get well" greeting card.',
            model="gemini-2.5-flash",
            instruction=(
                'You write customised "get well" greeting cards. '
                "You need to identity the name of the person "
                "to whom the card will be sent (the recipient), "
                "and the name of the person who will send the card "
                "(the sender). "
                'You also need to generate a customised "get well" '
                "message. In this customised message, assume the card "
                'has already started with "Dear recipient", '
                "so the message should not include a salutation. "
                "After determining the recipient, sender, and message, "
                "you must use the `write_get_well_message` tool "
                "to generate the final greeting card message."
            ),
            tools=[write_get_well_message],
        )
    except Exception:
        return None


def write_get_well_message(recipient: str, sender: str, message: str) -> str:
    """
    Writes a message suitable for a "get well" greeting card.

    Args:
        recipient (str): The name of the person to whom the message will be addressed.
        sender (str): The name of the person from whom the greeting card is sent.
        message (str): The customised "get well" message for the greeting card.

    Returns:
        the full text for the "get well" greeting card.
    """
    lines: list[str] = []
    lines.append(f"Dear {recipient},")
    lines.append(message)
    lines.append(f"From {sender}")
    lines.append("(get_well_writer)")
    return "\n".join(lines)
