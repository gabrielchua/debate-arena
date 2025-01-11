"""
Configuration settings for the debate application.
"""

# Available models for the debate
AVAILABLE_MODELS = ["o1", "gpt-4o", "gpt-4o-mini"]

# UI/Display settings
DEBATE_START_BANNER = "[bold white on blue]=== DEBATE START ===[/]"
MOTION_PANEL_STYLE = "yellow"
SPEAKER1_PANEL_STYLE = "blue"
SPEAKER2_PANEL_STYLE = "green"
FORFEIT_PANEL_STYLE = "red"
SPEAKER1_TEXT_STYLE = "bright_blue"
SPEAKER2_TEXT_STYLE = "bright_green"
FORFEIT_TEXT_STYLE = "bright_red"

# Speaker titles and labels
SPEAKER1_TITLE = "[red]🎙️ SPEAKER 1[/]"
SPEAKER2_TITLE = "[red]🎙️ SPEAKER 2[/]"


def get_system_message(speaker_num: int, side: str, motion: str) -> dict:
    """Generate the system message for a debate speaker."""
    ordinal = "st" if speaker_num == 1 else "nd"
    return {
        "role": "system",
        "content": f"""
                You are a skilled debater in a formal debate between you and the user.
                Your objective is to win by presenting compelling arguments for your position.
                Keep responses focused and impactful - aim for quality over quantity.
                Skip responding to weaker points to focus on key arguments.
                Avoid pleasantries and get straight to substance.
                Forfeit if you find yourself:
                - Agreeing with opponent's core arguments
                - Unable to counter their key points effectively 
                - Repeating previous arguments without advancing the debate
                - Losing the logical thread of your position

                Debate parameters:
                - Position: {speaker_num}{ordinal} speaker ({side})
                - Motion: {motion}
        """.strip(),
    }


# Opening prompt for first speaker
OPENING_PROMPT = (
    "You are opening this debate. Present your first argument in favor of the motion."
)

# Result messages
SPEAKER1_FORFEIT_MSG = (
    "\n[bold red]Speaker 1 (Proposition) forfeits! Speaker 2 (Opposition) wins.[/]"
)
SPEAKER2_FORFEIT_MSG = (
    "\n[bold red]Speaker 2 (Opposition) forfeits! Speaker 1 (Proposition) wins.[/]"
)

# UI Messages
MODELS_HEADER = "\n[bold cyan]🤖 Available Models:[/]"
SPEAKER1_CONFIG = "\n[bold magenta]🎙️ Speaker 1 Configuration[/]"
SPEAKER2_CONFIG = "\n[bold magenta]🎙️ Speaker 2 Configuration[/]"
DEBATE_SETUP = "\n[bold yellow]📢 Debate Setup[/]"
DEBATE_STATS = "\n[bold cyan]Debate Statistics:[/]"