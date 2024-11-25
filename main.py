import os
from dotenv import load_dotenv
from anki_generator import create_deck
import logging
from llm_processor import LLMProcessor


def main():
    """Main entry point for the Anki deck generation application."""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        load_dotenv()
        llm_processor = LLMProcessor()

        input_path = "data/sample.md"
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        create_deck(input_path, llm_processor)
        logger.info("Deck creation completed successfully")

    except Exception as e:
        logger.error(f"Error during deck creation: {str(e)}")
        raise


if __name__ == "__main__":
    main()
