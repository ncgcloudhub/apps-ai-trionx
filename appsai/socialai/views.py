import logging
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI  # Correct import for the OpenAI client
import chardet
from PyPDF2 import PdfFileReader
from io import BytesIO
from pdfminer.high_level import extract_text
import markdown
from PIL import Image
import pytesseract

# Setup logger
logger = logging.getLogger(__name__)

# Create an instance of the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def convert_markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html

def home(request):
    return render(request, 'socialai/home.html')

def contact(request):
    return render(request, 'socialai/contact.html')

def youtube_title_generator(request):
    return render(request, 'socialai/youtube_title_generator.html')

def youtube_tags_generator(request):
    return render(request, 'socialai/youtube_tags_generator.html')

def youtube_description_generator(request):
    return render(request, 'socialai/youtube_description_generator.html')

# Initialize the token count for the session
session_token_count = 0

# Initialize an empty chat history
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

@csrf_exempt
def chat(request):
    global chat_history, session_token_count

    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        files = request.FILES.getlist('file')
        file_names = [file.name for file in files]

        # Log user message and uploaded files
        logger.info(f"User message: {user_message}")
        logger.info(f"Uploaded files: {file_names}")

        if files:
            for file in files:
                file_content = file.read()
                file_type = file.content_type
                content = ""

                try:
                    if file_type == 'application/pdf':
                        content = extract_text(BytesIO(file_content))
                        logger.info("Extracted text from PDF")
                    elif file_type.startswith('image/'):
                        image = Image.open(BytesIO(file_content))
                        content = pytesseract.image_to_string(image)
                        logger.info("Extracted text from image")
                    else:
                        result = chardet.detect(file_content)
                        encoding = result['encoding'] or 'utf-8'
                        content = file_content.decode(encoding)
                        logger.info(f"Detected and decoded text from file with encoding: {encoding}")
                except Exception as e:
                    content = f"Unable to read file. Error: {str(e)}"
                    logger.error(f"Error reading file: {str(e)}")

                MAX_TOKENS = 128000
                if len(content) > MAX_TOKENS:
                    content = content[:MAX_TOKENS]
                    logger.warning("Truncated content to max tokens")

                chat_history.append({"role": "user", "content": f"{user_message}\n\n[File attached: {file.name}]"})

                try:
                    messages_to_send = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
                    ]
                    logger.debug(f"Messages to send: {messages_to_send}")

                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages_to_send
                        # messages=[
                        #     {"role": "system", "content": "You are a helpful assistant."},
                        #     {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
                        # ]
                    )
                    logger.debug(f"API response from OpenAI: {response}")

                    if response.choices and response.choices[0].message.content.strip():
                        summary = response.choices[0].message.content.strip()
                        summary_html = convert_markdown_to_html(summary)
                    else:
                        summary = "Unable to generate a summary."
                        summary_html = convert_markdown_to_html(summary)

                    # Update session token count
                    session_token_count += response.usage.total_tokens
                    logger.info(f"Tokens used in this response: {response.usage.total_tokens}")
                    logger.info(f"Total tokens used in session: {session_token_count}")

                except Exception as e:
                    logger.error(f"Error during OpenAI API call: {str(e)}")
                    summary = "Unable to generate a summary."
                    summary_html = convert_markdown_to_html(summary)

                chat_history.append({"role": "assistant", "content": summary_html})

        else:
            chat_history.append({"role": "user", "content": user_message})
            try:
                logger.debug(f"Messages to send to OpenAI: {chat_history}")

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=chat_history
                )
                logger.debug(f"API response from OpenAI-139: {response}")

                assistant_message = response.choices[0].message.content.strip()
                assistant_message_html = convert_markdown_to_html(assistant_message)
                chat_history.append({"role": "assistant", "content": assistant_message_html})

                 # Update session token count
                session_token_count += response.usage.total_tokens
                logger.info(f"Tokens used in this response: {response.usage.total_tokens}")
                logger.info(f"Total tokens used in session: {session_token_count}")
            except Exception as e:
                logger.error(f"Error during OpenAI API call: {str(e)}")
                chat_history.append({"role": "assistant", "content": "Unable to generate a message."})

        return redirect('chat')

    return render(request, 'socialai/chat.html', {'chat_history': chat_history})

@csrf_exempt
def upload_file(request):
    global chat_history

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_content = uploaded_file.read()

        logger.info("Received file upload: %s", uploaded_file.name)

        file_type = uploaded_file.content_type
        content = ""

        try:
            if file_type == 'application/pdf':
                content = extract_text(BytesIO(file_content))
                logger.info("Extracted text from PDF")
            elif file_type.startswith('image/'):
                image = Image.open(BytesIO(file_content))
                content = pytesseract.image_to_string(image)
                logger.info("Extracted text from image")
            else:
                result = chardet.detect(file_content)
                encoding = result['encoding'] or 'utf-8'
                content = file_content.decode(encoding)
                logger.info("Detected and decoded text from file with encoding: %s", encoding)
        except Exception as e:
            content = f"Unable to read file. Error: {str(e)}"
            logger.error("Error reading file: %s", e)

        MAX_TOKENS = 128000
        if len(content) > MAX_TOKENS:
            content = content[:MAX_TOKENS]
            logger.warning("Truncated content to max tokens")

        chat_history.append({"role": "user", "content": f"{content}"})

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
                ]
            )
            logger.debug(f"API response: {response}")

            summary = ""
            for chunk in response:
                if "choices" in chunk and chunk["choices"][0]["delta"]:
                    summary += chunk["choices"][0]["delta"].get("content", "")

            logger.info("Received response from OpenAI API")
            logger.debug("Summary generated: %s", summary)

            summary_html = convert_markdown_to_html(summary) if summary else "Unable to generate a summary."
            chat_history.append({"role": "assistant", "content": summary_html})
        except Exception as e:
            logger.error(f"Error during OpenAI API call: {str(e)}")
            chat_history.append({"role": "assistant", "content": "Unable to generate a summary."})

        return redirect('chat')

    return render(request, 'socialai/chat.html', {'chat_history': chat_history})
