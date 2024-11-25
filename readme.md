# Anki Flashcard Generator

An automated tool that generates Anki flashcards from text content using LLM (Language Learning Model) processing. The tool is particularly optimized for Hebrew-English content with RTL (Right-to-Left) support.

## Features

- Generates Anki flashcards from text content
- Supports Hebrew-English bilingual content
- RTL text formatting
- Customizable card templates
- LLM-powered content processing
- Stylish card design with modern CSS

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd anki-flashcard-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your LLM API credentials:
```
LLM_API_KEY=your_api_key_here (e.g: OPENAI_API_KEY=MYSECRETCODE)

```

## Usage

1. Place your source text file in the project directory.

2. Run the generator:
```python
from anki_generator import create_deck
from llm_processor import LLMProcessor

# Initialize the LLM processor
llm_processor = LLMProcessor()

# Generate the deck
create_deck("path/to/your/text/file.txt", llm_processor)
```

The generated Anki deck will be saved in the `result/` directory with the md file

## Card Format

The default card format follows this structure:
- Front: Question/Term in Hebrew
- Back: Detailed explanation in Hebrew
- Styling: RTL-optimized with modern CSS design

## Customization

You can customize the card generation by modifying the prompts in `prompts.py`. The default prompt creates challenging questions and comprehensive explanations.

### Custom Prompt Example

```python
custom_prompt = """
Your custom prompt format here
"""

llm_processor.generate_cards_content(content, custom_prompt)
```
