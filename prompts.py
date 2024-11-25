DEFAULT_ANKI_PROMPT = """
You are a harsh teacher, and you are grading your students on their ability to understand the material, and for that you are composing Anki flashcards for the course.
Create Anki flashcards from the following text. Each card should have:
1. A clear, concise question/term on the front
2. A comprehensive but focused explanation on the back
3. Write at least 25 cards
4. Make sure to include all the important points from the text as questions/terms, make them challenging and not obvious
5. Format each card as:
$Question/Term$
**הסבר**: Explanation

Text to process:
{text}
"""

CUSTOM_FORMAT_PROMPT = """
Create Anki flashcards from the following text using this specific format:
{custom_format}

Text to process:
{text}
"""
