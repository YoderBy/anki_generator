from typing import Optional, List, Tuple
from litellm import completion
import logging

logger = logging.getLogger(__name__)


class LLMProcessor:
    """
    Processes text through LLM to generate Anki cards content. Handles the interaction with LiteLLM
    and processes responses into a format suitable for Anki card generation.
    """

    def __init__(self, model: str = "gpt-4o", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    def generate_cards_content(
        self,
        text: str,
        prompt_template: str,
        max_tokens: Optional[int] = 2000
    ) -> str:
        """
        Generates Anki cards content using the specified LLM model. Processes input text according
        to the provided prompt template and returns formatted content for card creation.
        """
        try:
            logger.info(f"Generating cards content with model: {self.model}")
            response = completion(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt_template.format(text=text)
                }],
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error generating cards content: {str(e)}")
            raise
