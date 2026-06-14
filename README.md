# Greeting Card Writer

Greeting Card Writer is a small Python command-line sample for exploring
Google's Agent Development Kit. It accepts a short greeting-card request,
delegates the request to a specialist sub-agent, and prints a formatted card
message.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project is intentionally small so the ADK multi-agent workflow stays
visible. The main agent does not write the card directly. Instead, it acts as a
coordinator and delegates birthday, get-well, and sympathy card requests to
specialist writer agents.

## What It Does

The CLI accepts a prompt such as:

```powershell
.\.venv\Scripts\python.exe -m greeting_card_writer "Write a birthday card for Jenny from Fred"
```

The agent then:

- creates an in-memory ADK session
- creates specialist `birthday_writer`, `get_well_writer`, and
  `sympathy_writer` sub-agents
- sends the user's prompt to the main `greeting_card_writer` coordinator agent
- delegates supported card requests to the matching specialist sub-agent
- asks the specialist to identify the recipient, sender, and custom message
- calls the specialist's formatting tool to produce the final card text
- prints the final response

Each specialist has a narrow Python tool that formats the final card:

- `write_birthday_message`
- `write_get_well_message`
- `write_sympathy_message`

Unsupported card types should receive a response explaining that the agent is
unable to help with the request.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- A `GOOGLE_API_KEY` environment variable for Gemini model calls.

## Setup

Create the virtual environment and install the project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the card writer from the repository root:

```powershell
.\.venv\Scripts\python.exe -m greeting_card_writer "Write a birthday card for Jenny from Fred"
```

Example output:

```text
Dear Jenny,
Wishing you a wonderful birthday filled with joy, laughter, and happy memories.
From Fred
(birthday_writer)
```

The exact wording can vary between runs because delegation, message drafting,
and final response generation are model-driven.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/greeting_card_writer/
  __main__.py          Package entry point for python -m greeting_card_writer
  agent.py             Main ADK coordinator, runner, session, and CLI entry point
  birthday_writer.py   Birthday card specialist agent and formatting tool
  get_well_writer.py   Get-well card specialist agent and formatting tool
  sympathy_writer.py   Sympathy card specialist agent and formatting tool

tests/
  test_smoke.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is an ADK learning exercise, not a general-purpose card-writing
service. The supported card categories are deliberately limited so delegation
between the coordinator and specialist agents stays easy to see.

The formatting tools are simple local Python functions. The card category,
recipient, sender, and message content are still selected or inferred by
Gemini-backed ADK agents. Gemini API calls may incur usage costs.

## Third-Party Notices

This project has a direct runtime dependency on the `google-adk` Python package.
See the package's PyPI license metadata for full license and notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
