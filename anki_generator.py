from datetime import datetime
import logging
import genanki
import re
import random
import html
import os
import dotenv
from llm_processor import LLMProcessor
from prompts import DEFAULT_ANKI_PROMPT
dotenv.load_dotenv()
BASE_DIR = './result'
logger = logging.getLogger(__name__)


def generate_model_id():
    return random.randrange(1 << 30, 1 << 31)


def generate_deck_id():
    return random.randrange(1 << 30, 1 << 31)


def parse_input(text):
    entries = re.split(r'\n\n+', text.strip())
    cards = []
    for entry in entries:
        lines = entry.split('\n')
        headline_match = re.search(r'\$(.+?)\$', lines[0])

        if headline_match:
            # if there is a $, delete it
            headline = headline_match.group(1)
            headline = headline.replace('$', '')
        else:
            continue  # Skip this entry if no match is found
        explanation = ''
        for line in lines[1:]:
            if line.startswith('**הסבר**:'):
                explanation = line.replace('**הסבר**:', '').strip()
                break
        if headline and explanation:
            cards.append((headline, explanation))
    logger.info(f"Parsed {len(cards)} cards from the input text")
    return cards


def create_anki_deck(cards):
    model_id = generate_model_id()
    model = genanki.Model(
        model_id,
        'Hebrew-English RTL Stylish Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '''
                    <div class="card question">
                        <div class="content">{{Question}}</div>
                    </div>
                ''',
                'afmt': '''
                    <div class="card answer">
                        <div class="content">{{FrontSide}}</div>
                        <hr id="answer">
                        <div class="explanation">{{Answer}}</div>
                    </div>
                ''',
            },
        ],
        css='''
        .card {
            font-family: Arial, sans-serif;
            text-align: right;
            color: #333;
            background-color: #f0f0f0;
            direction: rtl;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .content {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .english {
            font-size: 18px;
            color: #7f8c8d;
            font-style: italic;
        }
        .explanation {
            font-size: 18px;
            line-height: 1.6;
            color: #34495e;
            margin-top: 15px;
        }
        hr {
            border: none;
            border-top: 2px solid #3498db;
            margin: 15px 0;
        }
        .answer {
            background-color: #e8f6f3;
        }
        '''
    )
    deck_id = generate_deck_id()
    deck = genanki.Deck(deck_id, 'Hebrew-English Genetics Deck')

    for front, back in cards:
        note = genanki.Note(
            model=model,
            fields=[html.escape(front), html.escape(back)]
        )
        deck.add_note(note)

    return deck


def create_deck(text_path: str, llm_processor: LLMProcessor) -> None:
    """Creates and saves an Anki deck from a text file using LLM processing.
    Coordinates the deck creation pipeline from file loading to deck generation."""
    # Create output directory if it doesn't exist
    os.makedirs(BASE_DIR, exist_ok=True)

    # Load and process content
    content = load_file(text_path)
    processed_content = llm_processor.generate_cards_content(
        content, DEFAULT_ANKI_PROMPT)

    # Generate cards and create deck
    cards = parse_input(processed_content)
    deck = create_anki_deck(cards)

    # Save the deck
    output_path = os.path.join(
        BASE_DIR, f'{datetime.now().strftime("%m-%d_%H-%M")}.apkg')
    deck.write_to_file(output_path)

    md_output = os.path.join(
        BASE_DIR, f'{datetime.now().strftime("%m-%d_%H-%M")}.md')
    with open(md_output, 'w', encoding='utf-8') as file:
        file.write(processed_content)
    logger.info(f"Deck saved to {output_path}")


def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
