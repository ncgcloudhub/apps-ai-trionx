# socialai/views.py:

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests
from bs4 import BeautifulSoup
#import OpenAI from openai
import os
from openai import OpenAI  # Correct import for the OpenAI client
import chardet
from PyPDF2 import PdfFileReader
from io import BytesIO
from pdfminer.high_level import extract_text
import markdown
from PIL import Image
import pytesseract

from django.shortcuts import render

# Create your views here.


# Create an instance of the OpenAI client
# Create an instance of the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def convert_markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html


def home(request):
    return render(request, 'socialai/home.html')

def home(request):
    return render(request, 'socialai/chat.html')

def contact(request):
    return render(request, 'socialai/contact.html')

def youtube_title_generator(request):
    return render(request, 'socialai/youtube_title_generator.html')

def youtube_tags_generator(request):
    return render(request, 'socialai/youtube_tags_generator.html')

def youtube_description_generator(request):
    return render(request, 'socialai/youtube_description_generator.html')

def tiktok_title_generator(request):
    return render(request, 'socialai/tiktok_title_generator.html')

def tiktok_tags_generator(request):
    return render(request, 'socialai/tiktok_tags_generator.html')

def tiktok_description_generator(request):
    return render(request, 'socialai/tiktok_description_generator.html')

def facebook_title_generator(request):
    return render(request, 'socialai/facebook_title_generator.html')

def facebook_tags_generator(request):
    return render(request, 'socialai/facebook_tags_generator.html')

def facebook_description_generator(request):
    return render(request, 'socialai/facebook_description_generator.html')

def instagram_title_generator(request):
    return render(request, 'socialai/instagram_title_generator.html')

def instagram_tags_generator(request):
    return render(request, 'socialai/instagram_tags_generator.html')

def instagram_description_generator(request):
    return render(request, 'socialai/instagram_description_generator.html')

def blog_title_generator(request):
    return render(request, 'socialai/blog_title_generator.html')

def blog_introduction_generator(request):
    return render(request, 'socialai/blog_introduction_generator.html')

def blog_conclusion_generator(request):
    return render(request, 'socialai/blog_conclusion_generator.html')

def blog_body_generator(request):
    return render(request, 'socialai/blog_body_generator.html')

def blog_tags_generator(request):
    return render(request, 'socialai/blog_tags_generator.html')

def vlog_title_generator(request):
    return render(request, 'socialai/vlog_title_generator.html')

def vlog_tags_generator(request):
    return render(request, 'socialai/vlog_tags_generator.html')

def vlog_description_generator(request):
    return render(request, 'socialai/vlog_description_generator.html')


def scrape_website(request):
    """
    View to scrape a website based on the URL provided by the user.
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url)
        data = ""

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.get_text()

        return render(request, 'socialai/scrape_result.html', {'data': data})
    return render(request, 'socialai/scrape_website.html')

def generate_content(request):
    """
    View to generate various types of content using OpenAI API.
    """
    if request.method == 'POST':
        prompt = request.POST.get('prompt')  # Get the prompt from the POST request
        content_type = request.POST.get('content_type')  # Get the content type from the POST request

        # Use the latest ChatCompletion method
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the model to use for generating content
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # System message
                {"role": "user", "content": f"Generate a {content_type} for: {prompt}"}  # User message with prompt and content type
            ]
        )
      
        generated_text = response.choices[0].message.content.strip()  # Get the generated text from the response
        return render(request, 'socialai/generate_result.html', {'generated_text': generated_text})  # Render the generated text in the template

    return render(request, 'socialai/generate_content.html')  # Render the generate_content.html template if the request method is not POST

def generate_tags(request):
    """
    View to generate tags using OpenAI API.
    """
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        # Use the latest ChatCompletion method
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate tags for: {prompt}"}
            ]
        )

        generated_text = response.choices[0].message.content.strip()
        return render(request, 'socialai/generate_result.html', {'generated_text': generated_text})

    return render(request, 'socialai/generate_tags.html')



    # def chat(request):
    #     """
    #     View to have a conversational chat with the OpenAI API.
    #     """
    #     if request.method == 'POST':
    #         message = request.POST.get('message')  # Get the user's message from the POST request

    #         # Use the latest ChatCompletion method
    #         response = client.chat.completions.create(
    #             model="gpt-4",
    #             messages=[
    #                 {"role": "system", "content": "You are a helpful assistant."},
    #                 {"role": "user", "content": message}  # User message
    #             ]
    #         )

    #         generated_text = response.choices[0].message.content.strip()
    #         return render(request, 'socialai/chat_result.html', {'generated_text': generated_text})

    #     return render(request, 'socialai/chat.html')

    # Initialize an empty chat history
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

@csrf_exempt
def chat(request):
    global chat_history

    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        files = request.FILES.getlist('file')
        file_names = [file.name for file in files]

        if files:
            for file in files:
                file_content = file.read()
                file_type = file.content_type
                content = ""

                try:
                    if file_type == 'application/pdf':
                        content = extract_text(BytesIO(file_content))
                    elif file_type.startswith('image/'):
                        image = Image.open(BytesIO(file_content))
                        content = pytesseract.image_to_string(image)
                    else:
                        result = chardet.detect(file_content)
                        encoding = result['encoding'] or 'utf-8'
                        content = file_content.decode(encoding)
                except Exception as e:
                    content = f"Unable to read file. Error: {str(e)}"
                
                MAX_TOKENS = 128000
                if len(content) > MAX_TOKENS:
                    content = content[:MAX_TOKENS]

                chat_history.append({"role": "user", "content": f"{user_message}\n\n[File attached: {file.name}]"})

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
                    ]
                )

                if response.choices and response.choices[0].message.content.strip():
                    summary = response.choices[0].message.content.strip()
                    summary_html = convert_markdown_to_html(summary)
                else:
                    summary = "Unable to generate a summary."
                    summary_html = convert_markdown_to_html(summary)

                chat_history.append({"role": "assistant", "content": summary_html})
        
        else:
            chat_history.append({"role": "user", "content": user_message})
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=chat_history
            )

            assistant_message = response.choices[0].message.content.strip()
            assistant_message_html = convert_markdown_to_html(assistant_message)
            chat_history.append({"role": "assistant", "content": assistant_message_html})

        return redirect('chat')

    return render(request, 'socialai/chat.html', {'chat_history': chat_history})


# #working one
@csrf_exempt
def upload_file(request):
    """
    View to handle file upload and use ChatGPT to summarize the file content.
    """
    global chat_history

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_content = uploaded_file.read()  # Read the content before saving the file

        # Detect file type based on MIME type
        file_type = uploaded_file.content_type

        content = ""

        try:
            if file_type == 'application/pdf':
                # Try to read PDF using pdfminer
                content = extract_text(BytesIO(file_content))
            elif file_type.startswith('image/'):
                # Try to read image using pytesseract
                image = Image.open(BytesIO(file_content))
                content = pytesseract.image_to_string(image)
            else:
                # Try to detect the file encoding for text files
                result = chardet.detect(file_content)
                encoding = result['encoding']
                if encoding is None:
                    encoding = 'utf-8'  # Use a default encoding if none was detected
                content = file_content.decode(encoding)
        except Exception as e:
            content = f"Unable to read file. Error: {str(e)}"
        
        # Truncate the content if it's too long
        MAX_TOKENS = 128000  # This is the maximum for gpt-4o
        if len(content) > MAX_TOKENS:
            content = content[:MAX_TOKENS]
        
        # Use the OpenAI API to summarize the file content
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
            ]
        )

        # Check if the model was able to generate a summary
        if response.choices and response.choices[0].message.content.strip():
            summary = response.choices[0].message.content.strip()
            summary_html = convert_markdown_to_html(summary)
        else:
            summary = "Unable to generate a summary."
            summary_html = convert_markdown_to_html(summary)
        chat_history.append({"role": "assistant", "content": summary_html})

        return redirect('chat')

    return render(request, 'socialai/chat.html', {'chat_history': chat_history})

# @csrf_exempt
# def chat(request):
#     """
#     View to handle continuous chat with the OpenAI API.
#     """
#     global chat_history

#     if request.method == 'POST':
#         user_message = request.POST.get('message')
#         chat_history.append({"role": "user", "content": user_message})

#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=chat_history
#         )

#         # Check if the model was able to generate a message
#         if response.choices and response.choices[0].message.content.strip():
#             assistant_message = response.choices[0].message.content.strip()
#             assistant_message_html = convert_markdown_to_html(assistant_message)
#         else:
#             assistant_message = "Unable to generate a message."
#             assistant_message_html = convert_markdown_to_html(assistant_message)

#         chat_history.append({"role": "assistant", "content": assistant_message_html})

#         return redirect('chat')  # Redirect to the same page to avoid resubmission

#     return render(request, 'socialai/chat.html', {'chat_history': chat_history})


# @csrf_exempt
# def upload_file(request):
#     """
#     View to handle file upload and use ChatGPT to process the file content.
#     """
#     global chat_history

#     if request.method == 'POST' and request.FILES['file']:
#         uploaded_file = request.FILES['file']
#         file_content = uploaded_file.read()  # Read the content before saving the file

#         # Detect file type based on MIME type
#         file_type = uploaded_file.content_type

#         content = ""

#         try:
#             if file_type == 'application/pdf':
#                 # Try to read PDF using pdfminer
#                 content = extract_text(BytesIO(file_content))
#             elif file_type.startswith('image/'):
#                 # Try to read image using pytesseract
#                 image = Image.open(BytesIO(file_content))
#                 content = pytesseract.image_to_string(image)
#             else:
#                 # Try to detect the file encoding for text files
#                 result = chardet.detect(file_content)
#                 encoding = result['encoding']
#                 if encoding is None:
#                     encoding = 'utf-8'  # Use a default encoding if none was detected
#                 content = file_content.decode(encoding)
#         except Exception as e:
#             content = f"Unable to read file. Error: {str(e)}"
        
#         # Truncate the content if it's too long
#         MAX_TOKENS = 128000  # This is the maximum for gpt-4o
#         if len(content) > MAX_TOKENS:
#             content = content[:MAX_TOKENS]
        
#         # Ask the assistant what to do with the uploaded document
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": f"A document has been uploaded. Here is the content:\n\n{content}\n\nWhat would you like to do with this document?"}
#             ]
#         )

#         assistant_message = response.choices[0].message.content.strip()
#         chat_history.append({"role": "assistant", "content": convert_markdown_to_html(assistant_message)})

#         return redirect('chat')

#     return render(request, 'socialai/chat.html', {'chat_history': chat_history})
