"""
reply.py

This file contains the Reply class, which is used to represent the response of a speaker in a debate.
"""

# Third-party imports
from pydantic import BaseModel, Field


class Reply(BaseModel):
    """
    Represents the response of a speaker in a debate.

    Attributes:
        planning (str): The planning and strategy details for the debate response, based on the opponent's arguments
        to_forfeit_debate (bool): Flag indicating whether to forfeit the debate
        response (str | None): The actual debate response text, null if forfeiting. Keep your response less than 500 characters.
        reason_for_forfeit (str | None): The reason for forfeiting the debate, null if not forfeiting. Be specific about why you are forfeiting. Keep your response less than 500 characters.
    """

    planning: str = Field(
        description="The planning and strategy details for the debate response, based on the opponent's arguments"
    )
    response: str | None = Field(
        default=None,
        description="The actual debate response text. Can be null if you intend to forfeit the debate. Keep your response less than 500 characters.",
        max_length=500,
    )
    are_you_repeating_previous_arguments: bool = Field(
        description="Flag indicating whether you are about torepeating previous arguments"
    )
    reason_for_forfeit: str | None = Field(
        default=None,
        description="The reason for forfeiting the debate. Can be null if you do not intend to forfeit the debate. Be specific about why you are forfeiting. Keep your response less than 500 characters.",
        max_length=500,
    )
    to_forfeit_debate: bool = Field(
        description="Flag indicating whether to forfeit the debate"
    )

    @property
    def response_text(self):
        if self.to_forfeit_debate:
            return None
        return self.response

    @property
    def reason_for_forfeit_text(self):
        if not self.to_forfeit_debate:
            return None
        return self.reason_for_forfeit
