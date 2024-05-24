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


# Create your views here.


# Create an instance of the OpenAI client
# Create an instance of the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def convert_markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html

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
    """
    View to handle continuous chat with the OpenAI API.
    """
    global chat_history

    if request.method == 'POST':
        user_message = request.POST.get('message')
        chat_history.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )

        assistant_message = response.choices[0].message.content.strip()
        #assistant_message = assistant_message.replace('\n', '<br>')
        chat_history.append({"role": "assistant", "content": assistant_message})

        return redirect('chat')  # Redirect to the same page to avoid resubmission

    return render(request, 'socialai/chat.html', {'chat_history': chat_history})

# @csrf_exempt
# def upload_file(request):
#     """
#     View to handle file upload and use ChatGPT to summarize the file content.
#     """
#     global chat_history

#     if request.method == 'POST' and request.FILES['file']:
#         uploaded_file = request.FILES['file']
#         file_content = uploaded_file.read()  # Read the content before saving the file

#         file_name = default_storage.save(uploaded_file.name, ContentFile(file_content))
#         file_path = default_storage.path(file_name)

#         # Now you can open the file
#         with open(file_path, 'rb') as file:
#             response = client.files.create(
#                 file=file,
#                 purpose="assistants"
#             )
#         file_id = response.id


#         # Try to detect the file encoding
#         result = chardet.detect(file_content)
#         encoding = result['encoding']

#         if encoding is None:
#             encoding = 'utf-8'  # Use a default encoding if none was detected

#         try:
#             # Try to decode the file content
#             content = file_content.decode(encoding)
#         except UnicodeDecodeError:
#             # If that fails, try to read it as a PDF
#             try:
#                 reader = PdfFileReader(BytesIO(file_content))
#                 content = ''
#                 for page in range(reader.getNumPages()):
#                     content += reader.getPage(page).extractText()
#             except Exception as e:
#                 content = "Unable to read file"
        
#         # Truncate the content if it's too long
#         MAX_TOKENS = 128000  # This is the maximum for gpt-4o
#         if len(content) > MAX_TOKENS:
#             content = content[:MAX_TOKENS]

        
#         # Use the OpenAI API to summarize the file content
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": content}
#             ]
#         )

#         # Check if the model was able to generate a summary
#         if response.choices and response.choices[0].message.content.strip():
#             summary = response.choices[0].message.content.strip()
#         else:
#             summary = "Unable to generate a summary."
#         chat_history.append({"role": "assistant", "content": summary})

#         return redirect('chat')

#     return render(request, 'socialai/chat.html', {'chat_history': chat_history})


@csrf_exempt
def upload_file(request):
    """
    View to handle file upload and use ChatGPT to summarize the file content.
    """
    global chat_history

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_content = uploaded_file.read()  # Read the content before saving the file

        # Try to detect the file encoding
        result = chardet.detect(file_content)
        encoding = result['encoding']

        if encoding is None:
            encoding = 'utf-8'  # Use a default encoding if none was detected

        try:
            # Try to decode the file content
            content = file_content.decode(encoding)
        except (UnicodeDecodeError, AttributeError):
            # If that fails, try to read it as a PDF using pdfminer
            try:
                content = extract_text(BytesIO(file_content))
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