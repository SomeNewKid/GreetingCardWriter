from __future__ import annotations

from google.adk.agents import Agent


def create_birthday_writer() -> Agent | None:
    try:
        return Agent(
            name="birthday_writer",
            description='Writes a "birthday" greeting card.',
            model="gemini-2.5-flash",
            instruction=(
                'You write customised "birthday" greeting cards. '
                "You need to identity the name of the person "
                "to whom the card will be sent (the recipient), "
                "and the name of the person who will send the card "
                "(the sender). "
                'You also need to generate a customised "birthday" '
                "message. In this customised message, assume the card "
                'has already started with "Dear recipient", '
                "so the message should not include a salutation. "
                "After determining the recipient, sender, and message, "
                "you must use the `write_birthday_message` tool "
                "to generate the final greeting card message."
            ),
            tools=[write_birthday_message],
        )
    except Exception:
        return None


def write_birthday_message(recipient: str, sender: str, message: str) -> str:
    """
    Writes a message suitable for a "birthday" greeting card.

    Args:
        recipient (str): The name of the person to whom the message will be addressed.
        sender (str): The name of the person from whom the greeting card is sent.
        message (str): The customised "birthday" message for the greeting card.

    Returns:
        the full text for the "birthday" greeting card.
    """
    lines: list[str] = []
    lines.append(f"Dear {recipient},")
    lines.append(message)
    lines.append(f"From {sender}")
    lines.append("(birthday_writer)")
    return "\n".join(lines)
