"""
app.py
"""

# Third-party imports
import instructor
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from simple_term_menu import TerminalMenu
from typing import List, Dict

# Local imports
import config
from reply import Reply

# Patch the OpenAI client
speaker1 = instructor.from_openai(OpenAI())
speaker2 = instructor.from_openai(OpenAI())

# Initialize the terminal console
console = Console()


def handle_forfeit(reply: Reply, speaker_title: str, turn_count: int) -> None:
    """
    Prints forfeit information to the console.

    Args:
        reply (Reply): The reply object containing forfeit information.
        speaker_title (str): The title of the speaker who forfeited.
        turn_count (int): The total number of turns in the debate.

    Returns:
        None
    """
    console.print(f"{config.DEBATE_STATS}\nTotal turns: {turn_count}")
    console.print(
        Panel(
            Text(reply.reason_for_forfeit_text, style=config.FORFEIT_TEXT_STYLE),
            title=f"{speaker_title} (Turn {turn_count})",
            border_style=config.FORFEIT_PANEL_STYLE,
        )
    )


def perform_speaker_turn(
    speaker,
    speaker_messages: List[Dict[str, str]],
    user_prompt: str,
    model: str,
    speaker_title: str,
    text_style: str,
    panel_style: str,
    turn_count: int,
) -> Reply:
    """
    Performs a single speaker's turn by sending the user's prompt (or last opponent's
    argument) to the model and retrieving the reply.

    Args:
        speaker: The speaker (wrapped openai client).
        speaker_messages (List[Dict[str, str]]): Accumulated conversation messages for this speaker.
        user_prompt (str): The user prompt or opponent's last statement.
        model (str): The model name.
        speaker_title (str): Panel title to display in the console.
        text_style (str): The rich text style for displaying the speaker's response.
        panel_style (str): The rich panel style for the speaker's response.
        turn_count (int): The current turn number.

    Returns:
        Reply: The generated reply object.
    """
    reply = speaker.chat.completions.create(
        model=model,
        response_model=Reply,
        messages=speaker_messages + [{"role": "user", "content": user_prompt}],
    )

    # If not a forfeit, print the speaker's response and append it to messages
    if not reply.to_forfeit_debate:
        console.print(
            Panel(
                Text(reply.response, style=text_style),
                title=f"{speaker_title} (Turn {turn_count})",
                border_style=panel_style,
            )
        )
        speaker_messages.append({"role": "assistant", "content": reply.response})

    return reply


def debate(motion: str, speaker1_model: str, speaker2_model: str) -> str:
    """
    Conduct a debate between two speakers.

    Args:
        motion (str): The motion of the debate.
        speaker1_model (str): The model for the first speaker.
        speaker2_model (str): The model for the second speaker.

    Returns:
        str: The result of the debate.
    """

    # Initialize conversation history for both speakers
    speaker1_messages = [config.get_system_message(1, "proposition", motion)]
    speaker2_messages = [config.get_system_message(2, "opposition", motion)]

    console.print(f"\n{config.DEBATE_START_BANNER}")
    console.print(
        Panel(
            f"[bold yellow]{motion}",
            title="Motion",
            border_style=config.MOTION_PANEL_STYLE,
        )
    )
    console.print()

    turn_count = 0

    # Speaker 1's opening argument
    turn_count += 1  # Increment turn count
    reply1 = perform_speaker_turn(
        speaker=speaker1,
        speaker_messages=speaker1_messages,
        user_prompt=config.OPENING_PROMPT,
        model=speaker1_model,
        speaker_title=config.SPEAKER1_TITLE,
        text_style=config.SPEAKER1_TEXT_STYLE,
        panel_style=config.SPEAKER1_PANEL_STYLE,
        turn_count=turn_count,
    )

    # Check for forfeit
    if reply1.to_forfeit_debate:
        handle_forfeit(reply1, config.SPEAKER1_TITLE, turn_count)
        return config.SPEAKER1_FORFEIT_MSG

    # Debate loop
    while True:
        # Speaker 2's turn (responds to Speaker 1's latest statement)
        turn_count += 1  # Increment turn count
        last_speaker1_content = speaker1_messages[-1]["content"]
        reply2 = perform_speaker_turn(
            speaker=speaker2,
            speaker_messages=speaker2_messages,
            user_prompt=last_speaker1_content,
            model=speaker2_model,
            speaker_title=config.SPEAKER2_TITLE,
            text_style=config.SPEAKER2_TEXT_STYLE,
            panel_style=config.SPEAKER2_PANEL_STYLE,
            turn_count=turn_count,
        )

        # Check for forfeit
        if reply2.to_forfeit_debate:
            handle_forfeit(reply2, config.SPEAKER2_TITLE, turn_count)
            return config.SPEAKER2_FORFEIT_MSG

        # Append the last speaker2 content as the next user prompt for speaker1
        speaker1_messages.append({"role": "user", "content": reply2.response})

        # Speaker 1's turn (responds to Speaker 2's latest statement)
        turn_count += 1  # Increment turn count
        last_speaker2_content = speaker2_messages[-1]["content"]
        reply1 = perform_speaker_turn(
            speaker=speaker1,
            speaker_messages=speaker1_messages,
            user_prompt=last_speaker2_content,
            model=speaker1_model,
            speaker_title=config.SPEAKER1_TITLE,
            text_style=config.SPEAKER1_TEXT_STYLE,
            panel_style=config.SPEAKER1_PANEL_STYLE,
            turn_count=turn_count,
        )

        # Check for forfeit
        if reply1.to_forfeit_debate:
            handle_forfeit(reply1, config.SPEAKER1_TITLE, turn_count)
            return config.SPEAKER1_FORFEIT_MSG

        # Append the last speaker1 content as the next user prompt for speaker2
        speaker2_messages.append({"role": "user", "content": reply1.response})


if __name__ == "__main__":

    console.print(config.SPEAKER1_CONFIG)
    terminal_menu = TerminalMenu(
        config.AVAILABLE_MODELS, title="Select model for Speaker 1"
    )
    menu_entry_index = terminal_menu.show()
    speaker1_model = config.AVAILABLE_MODELS[menu_entry_index]
    console.print(f"Selected: [bold magenta]{speaker1_model}[/]")

    console.print(config.SPEAKER2_CONFIG)
    terminal_menu = TerminalMenu(
        config.AVAILABLE_MODELS, title="Select model for Speaker 2"
    )
    menu_entry_index = terminal_menu.show()
    speaker2_model = config.AVAILABLE_MODELS[menu_entry_index]
    console.print(f"Selected: [bold magenta]{speaker2_model}[/]")

    console.print(config.DEBATE_SETUP)
    motion = input("Enter the debate motion: ")
    result = debate(motion, speaker1_model, speaker2_model)
    console.print(result)
