import os
import streamlit as st
from openai import AsyncOpenAI
import json
import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
import PyPDF2
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import re

async def get_response(chapter, font_size, lineheight, language, font_style, font_path):
  # Set up OpenAI API client
  client = AsyncOpenAI(api_key = st.secrets["Openai_api"])
  font_size_px = f"{font_size}px"
  line_height_val = str(lineheight)
  max_chars = 35000
  # Set up OpenAI model and prompt
  model="gpt-4o-mini-2024-07-18"
  # Split the chapter into two parts based on character count
  if len(chapter) <= max_chars:
    # If the chapter is within the limit, process normally
    prompt_template = """You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.
14. The chapter heading can be anything like just a number or roman numeral and can also include just special characters like Chapter ^. 
15. Do not make any changes to the provided chapter heading and use the heading as it is given only. Do not write the word chapter before the heading if it is not given.
16. Make sure to include the entire text given as input in the html. You can check this by checking the last line of the response and the input. Dont write anything about this in the repsonse.
I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”


This is the sample HTML : <!DOCTYPE html>
<html lang="<<lang>>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>

        @font-face {
            font-family: <<font_style>>;
            src: url(<<font_path>>) format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        body {
            font-family: <<font_style>>, serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 20vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    </body>
  </html>

    Here is the target chapter: <<CHAPTER_TEXT>>"""
    lan = 'en' if language == "English" else 'hi'
    prompt = prompt_template.replace("<<CHAPTER_TEXT>>", chapter).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val).replace("<<lang>>", lan).replace("<<font_style>>", font_style).replace("<<font_path>>", font_path)
    chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0
        )
    
    if chat_completion.choices[0].finish_reason != "content_filter":
        response = chat_completion.choices[0].message.content
    else:
        client = AsyncOpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key = st.secrets["Mistral_api"],
        )
        
        chat_completion = await client.chat.completions.create(
          model="mistralai/codestral-2501",
          messages=[
            {
              "role": "user",
              "content": prompt
            }
          ]
        )
        response = chat_completion.choices[0].message.content
    return response

  elif(len(chapter) > max_chars and len(chapter) <= 70000):
        # If the chapter exceeds the limit, split into two parts
        split_pos = chapter.rfind('.', 0, max_chars)
        first_part = chapter[:split_pos + 1]
        second_part = chapter[split_pos + 1:]

        # Process the first part normally
        prompt_template_1 = """
        You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.
14. The chapter heading can be anything like just a number or roman numeral and can also include just special characters like Chapter ^. 
15. Do not make any changes to the provided chapter heading and use the heading as it is given only. Do not write the word chapter before the heading if it is not given.
16. Make sure to include the entire text given as input in the html. You can check this by checking the last line of the response and the input. Dont write anything about this in the repsonse.
I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”


This is the sample HTML : <!DOCTYPE html>
<html lang="<<lang>>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>

        @font-face {
            font-family: <<font_style>>;
            src: url(<<font_path>>) format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        body {
            font-family: <<font_style>>, serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 20vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    </body>
  </html>

    Here is the target chapter: <<CHAPTER_TEXT>>
        """
        lan = 'en' if language == "English" else 'hi'
        prompt_1 = prompt_template_1.replace("<<CHAPTER_TEXT>>", first_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val).replace("<<lang>>", lan).replace("<<font_style>>", font_style).replace("<<font_path>>", font_path)

        chat_completion_1 = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_1,
                }
            ],
            model=model,
            temperature=0
        )
        if chat_completion_1.choices[0].finish_reason != "content_filter":
            response_1 = chat_completion_1.choices[0].message.content
        else:
            client = AsyncOpenAI(
              base_url="https://openrouter.ai/api/v1",
              api_key = st.secrets["Mistral_api"],
            )
            
            chat_completion_1 = await client.chat.completions.create(
              model="mistralai/codestral-2501",
              messages=[
                {
                  "role": "user",
                  "content": prompt_1
                }
              ]
            )
            response_1 = chat_completion_1.choices[0].message.content

        

        # Process the second part with a modified prompt (no HTML headers)
        prompt_template_2 = """
        You are an expert book formatter.
        Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
        Font size = <<fontsize>>
        Line height = <<lineheight>>
        <html lang="<<lang>>">
        Include these features in html:
        1. Paragraph Formatting
        Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
        2. Line Length
        Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
        3.Line Spacing (Leading)
        Comfortable Reading: The line spacing should be the same as given in the example.
        4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
        8. Left and Right margins are minimum so the pdf looks like a book.
        7.  Consistency
        Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
        8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
        9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
        Keep this in mind : Left and Right margins are minimum.
        10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
        11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

        Here is the continuation of the chapter:
        <<CHAPTER_TEXT>>
        """
        lan = 'en' if language == "English" else 'hi'
        prompt_2 = prompt_template_2.replace("<<CHAPTER_TEXT>>", second_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val).replace("<<lang>>", lan)

        chat_completion_2 = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_2,
                }
            ],
            model=model,
            temperature=0
        )

        if chat_completion_2.choices[0].finish_reason != "content_filter":
            response_2 = chat_completion_2.choices[0].message.content
        else:
            client = AsyncOpenAI(
              base_url="https://openrouter.ai/api/v1",
              api_key = st.secrets["Mistral_api"],
            )
            
            chat_completion_2 = await client.chat.completions.create(
              model="mistralai/codestral-2501",
              messages=[
                {
                  "role": "user",
                  "content": prompt_2
                }
              ]
            )
            response_2 = chat_completion_2.choices[0].message.content

        # Now, merge the two responses
        # Extract the <body> content from the first response and append the second response

        # Find the closing </body> and </html> tags in the first response
        body_close_index = response_1.rfind("</body>")
        html_close_index = response_1.rfind("</html>")

        if body_close_index != -1:
            # Insert the second response before the closing </body> tag
            merged_html = response_1[:body_close_index] + "\n" + response_2 + "\n" + response_1[body_close_index:]
        elif html_close_index != -1:
            # Insert before </html> if </body> is not found
            merged_html = response_1[:html_close_index] + "\n" + response_2 + "\n" + response_1[html_close_index:]
        else:
            # If no closing tags are found, simply concatenate
            merged_html = response_1 + "\n" + response_2

        return merged_html
    
  else:
        # If the chapter exceeds the limit, split into two parts
        split_pos_1 = chapter.rfind('.', 0, max_chars)
        split_pos_2 = chapter.rfind('.', max_chars, 70000)
        first_part = chapter[:split_pos_1 + 1]
        second_part = chapter[split_pos_1 + 1 : split_pos_2 + 1]
        third_part = chapter[split_pos_2 + 1:]
        # Process the first part normally
        prompt_template_1 = """
        You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.
14. The chapter heading can be anything like just a number or roman numeral and can also include just special characters like Chapter ^. 
15. Do not make any changes to the provided chapter heading and use the heading as it is given only. Do not write the word chapter before the heading if it is not given.
16. Make sure to include the entire text given as input in the html. You can check this by checking the last line of the response and the input. Dont write anything about this in the repsonse.
I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.

“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.
“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.
“Just trying to process your depth, Mr. Malhotra.”
“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”
“You’re such a terrific musician. Why don’t you want to do something with your talent?”
“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”
She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”

****

After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
house in Sainik Farms. They would talk for hours, listen to new records, order in food and
watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
and sat there on the uneven concrete floor watching the sun setting behind the horizon,
staining the sky blood red.
&quot;I was sixteen when my dad died.&quot; She stared into nothingness as she spoke, and it seemed as
though words came out of her mouth without her consent. The shadow of her hair falling on
her bony face danced on her cheek as slight darkness began to set in.
Dhruv was surprised at her sudden confession. She never told him much about her family and
was unusually reserved when it came to her parents. But that day, she looked
uncharacteristically sad as she continued talking.
&quot;It was cancer.”


This is the sample HTML : <!DOCTYPE html>
<html lang="<<lang>>">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>

        @font-face {
            font-family: <<font_style>>;
            src: url(<<font_path>>) format('truetype');
            font-weight: normal;
            font-style: normal;
        }

        body {
            font-family: <<font_style>>, serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 20vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    
    <p>“Wow! That’s deep.” Anisha stood there, looking at him intently for a few minutes.</p>
    <p>“Why so serious, Ms Sighania?” He said whimsically, to lighten the air.</p>
    <p>“Just trying to process your depth, Mr. Malhotra.”</p>
    <p>“It’s not that serious man.” He chuckled, “I mean, I am decent at math so maybe I can work
    at a bank.” He chuckled. “ Buy and sell stocks. Work on deals. I don’t know.”</p>
    <p>“You’re such a terrific musician. Why don’t you want to do something with your talent?”</p>
    <p>“I don’t know. I guess I don’t want to play for the world. I want to keep this only for myself.”</p>
    <p>She took a moment to absorb his ideas and then suddenly stood up. “Can we smoke?”</p>

    <p>****</p>

    <p>After that day, they began to hang out often. Anisha became a regular visitor at the Malhotra
    house in Sainik Farms. They would talk for hours, listen to new records, order in food and
    watch movies. One evening when Anisha was unusually quiet, they went up to the terrace
    and sat there on the uneven concrete floor watching the sun setting behind the horizon,
    staining the sky blood red.
    “I was sixteen when my dad died.” She stared into nothingness as she spoke, and it seemed as
    though words came out of her mouth without her consent. The shadow of her hair falling on
    her bony face danced on her cheek as slight darkness began to set in.</p>
    <p>Dhruv was surprised at her sudden confession. She never told him much about her family and
    was unusually reserved when it came to her parents. But that day, she looked
    uncharacteristically sad as she continued talking.</p>
    <p>“It was cancer.”</p>
    </body>
  </html>

    Here is the target chapter: <<CHAPTER_TEXT>>
        """
        lan = 'en' if language == "English" else 'hi'
        prompt_1 = prompt_template_1.replace("<<CHAPTER_TEXT>>", first_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val).replace("<<lang>>", lan).replace("<<font_style>>", font_style).replace("<<font_path>>", font_path)

        chat_completion_1 = await client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_1,
              }
          ],
          model=model,
          temperature=0
      )

        if chat_completion_1.choices[0].finish_reason != "content_filter":
            response_1 = chat_completion_1.choices[0].message.content
        else:
            client = AsyncOpenAI(
              base_url="https://openrouter.ai/api/v1",
              api_key = st.secrets["Mistral_api"],
            )
            
            chat_completion_1 = await client.chat.completions.create(
              model="mistralai/codestral-2501",
              messages=[
                {
                  "role": "user",
                  "content": prompt_1
                }
              ]
            )
            response_1 = chat_completion_1.choices[0].message.content

      # Process the second part with a modified prompt (no HTML headers)
        prompt_template_2 = """
      You are an expert book formatter.
      Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
      Font size = <<fontsize>>
      Line height = <<lineheight>>
      <html lang="<<lang>>">
      Include these features in html:
      1. Paragraph Formatting
      Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
      2. Line Length
      Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
      3.Line Spacing (Leading)
      Comfortable Reading: The line spacing should be the same as given in the example.
      4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
      8. Left and Right margins are minimum so the pdf looks like a book.
      7.  Consistency
      Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
      8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
      9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
      Keep this in mind : Left and Right margins are minimum.
      10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
      11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

      Here is the continuation of the chapter:
      <<CHAPTER_TEXT>>
      """
        lan = 'en' if language == "English" else 'hi'
        prompt_2 = prompt_template_2.replace("<<CHAPTER_TEXT>>", second_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_2 = await client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_2,
              }
          ],
          model=model,
          temperature=0
      )

        if chat_completion_2.choices[0].finish_reason != "content_filter":
            response_2 = chat_completion_2.choices[0].message.content
        else:
            client = AsyncOpenAI(
              base_url="https://openrouter.ai/api/v1",
              api_key = st.secrets["Mistral_api"],
            )
            
            chat_completion_2 = await client.chat.completions.create(
              model="mistralai/codestral-2501",
              messages=[
                {
                  "role": "user",
                  "content": prompt_2
                }
              ]
            )
            response_2 = chat_completion_2.choices[0].message.content

        # Process the second part with a modified prompt (no HTML headers)
        prompt_template_3 = """
      You are an expert book formatter.
      Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
      Font size = <<fontsize>>
      Line height = <<lineheight>>
      <html lang="<<lang>>">
      Include these features in html:
      1. Paragraph Formatting
      Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
      2. Line Length
      Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
      3.Line Spacing (Leading)
      Comfortable Reading: The line spacing should be the same as given in the example.
      4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
      8. Left and Right margins are minimum so the pdf looks like a book.
      7.  Consistency
      Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
      8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
      9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
      Keep this in mind : Left and Right margins are minimum.
      10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
      11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

      Here is the continuation of the chapter:
      <<CHAPTER_TEXT>>
      """
        lan = 'en' if language == "English" else 'hi'
        prompt_3 = prompt_template_3.replace("<<CHAPTER_TEXT>>", third_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val).replace("<<lang>>", lan)

        chat_completion_3 = await client.chat.completions.create(
          messages=[
              {
                  "role": "user",
                  "content": prompt_3,
              }
          ],
          model=model,
          temperature=0
      )

        if chat_completion_3.choices[0].finish_reason != "content_filter":
            response_3 = chat_completion_3.choices[0].message.content
        else:
            client = AsyncOpenAI(
              base_url="https://openrouter.ai/api/v1",
              api_key = st.secrets["Mistral_api"],
            )
            
            chat_completion_3 = await client.chat.completions.create(
              model="mistralai/codestral-2501",
              messages=[
                {
                  "role": "user",
                  "content": prompt_3
                }
              ]
            )
            response_3 = chat_completion_3.choices[0].message.content

        # Now, merge the two responses
        # Extract the <body> content from the first response and append the second response

        # Find the closing </body> and </html> tags in the first response
        body_close_index = response_1.rfind("</body>")
        html_close_index = response_1.rfind("</html>")

        if body_close_index != -1:
          # Insert the second response before the closing </body> tag
          merged_html = response_1[:body_close_index] + "\n" + response_2 + "\n" + response_3 + "\n" + response_1[body_close_index:]
        elif html_close_index != -1:
          # Insert before </html> if </body> is not found
          merged_html = response_1[:html_close_index] + "\n" + response_2 + "\n" + response_3 + "\n" + response_1[html_close_index:]
        else:
          # If no closing tags are found, simply concatenate
          merged_html = response_1 + "\n" + response_2 + "\n" + response_3

        return merged_html

	
def save_response(response):
    html_pth = 'neww.html'
    with open(html_pth, 'w', encoding='utf-8') as file:
        file.write(response)
    return html_pth


nest_asyncio.apply()

async def html_to_pdf_with_margins(html_file, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        await page.set_content(html_content, wait_until='networkidle')

        pdf_options = {
            'path': output_pdf,
            'format': 'A4',
            'margin': {
                'top': '85px',
                'bottom': '60px',
                'left': '70px',
                'right': '40px'
            },
            'print_background': True
        }

        await page.pdf(**pdf_options)
        await browser.close()

def get_pdf_page_count(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)
    
def create_overlay_pdf(overlay_pdf, total_pages, starting_page_number, book_name, author_name, font_style, font_path, current_position):
    c = canvas.Canvas(overlay_pdf, pagesize=A4)
    width, height = 130 * mm, 197 * mm  # Correctly converting mm to points
    custom_font_name = font_style
    pdfmetrics.registerFont(TTFont(custom_font_name, font_path))

    def draw_header_footer(page_number, position):
        c.setFont(custom_font_name, 12)

        if page_number == starting_page_number:
            # First page of the chapter: Draw page number at the bottom center
            footer_y = 25  # Adjust this value to match the bottom text's baseline
            c.drawCentredString(width / 2, footer_y, f'{page_number}')
        elif position == "Right":
            # Right-side pages: Draw header on the right and page number at the right
            c.drawCentredString(width / 2, height - 35, book_name)
            c.drawString(width - 84, height - 35, f'{page_number}')  # Adjusted x-coordinate for gap
        elif position == "Left":
            # Left-side pages: Draw header on the left and page number at the left
            c.drawCentredString(width / 2, height - 35, author_name)
            c.drawString(62, height - 35, f'{page_number}')  # Adjusted x-coordinate for gap

    # Create pages for the overlay
    for i in range(total_pages):
        current_page_number = starting_page_number + i  # Continuous page numbering
        draw_header_footer(current_page_number, current_position)

        # Alternate position for the next page
        current_position = "Left" if current_position == "Right" else "Right"

        c.showPage()

    c.save()

    # Return the final position for the next chapter
    return current_position

def overlay_headers_footers(main_pdf, overlay_pdf, output_pdf):
    pdf_writer = PdfWriter()

    # Load the main PDF and the overlay PDF
    with open(main_pdf, 'rb') as main_file, open(overlay_pdf, 'rb') as overlay_file:
        main_pdf_reader = PdfReader(main_file)
        overlay_pdf_reader = PdfReader(overlay_file)

        # Ensure the overlay PDF has the same number of pages as the main PDF
        print(len(overlay_pdf_reader.pages))
        print(len(main_pdf_reader.pages))
        if len(overlay_pdf_reader.pages) != len(main_pdf_reader.pages):
            raise ValueError("The number of pages in the overlay PDF does not match the number of pages in the main PDF.")

        # Overlay headers and footers on each page
        for page_num in range(len(main_pdf_reader.pages)):
            main_page = main_pdf_reader.pages[page_num]
            overlay_page = overlay_pdf_reader.pages[page_num]

            # Merge the overlay onto the main page
            main_page.merge_page(overlay_page)

            pdf_writer.add_page(main_page)

    # Write the combined PDF to the output file
    with open(output_pdf, 'wb') as outfile:
        pdf_writer.write(outfile)




def modify_element(element, html_path):
    
    with open(html_path, 'r', encoding='utf-8') as file:
        content = file.read()
    for ele in element:
        if ele["text"] in content:
            style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
            if style_match:
                style_content = style_match.group(1)
                phrase = ele["text"]
                font_style = ele["font_style"]
                font_size = ele["font_size"]
                font_class = font_style.replace(" ", "-").lower()
                font_face_rule = f"""
                @font-face {{
                    font-family: "{font_style}";
                    src: url("fonts/{font_style}.ttf") format("truetype");
                    font-weight: normal;
                    font-style: normal;
                }}
                
                .{font_class} {{
                    font-family: "{font_style}", serif;
                    font-size: {font_size}px;
                }}
                """
                style_content += font_face_rule
                span_tag = f'<span class="{font_class}">{phrase}</span>'
                content = content.replace(phrase, span_tag)
                new_style_block = f'<style>{style_content}</style>'
                content = re.sub(r'<style>.*?</style>', new_style_block, content, flags=re.DOTALL)
                with open(html_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            
            