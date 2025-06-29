from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from config.firebase import db

from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import CustomUser
import hashlib

from django.contrib import messages  # Import messages module
from django.shortcuts import render, redirect
from .models import CustomUser
import hashlib


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save the user
        CustomUser.objects.create(username=username, email=email, password=hashed_password)
        return redirect('login')  # Redirect to login after successful registration

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = CustomUser.objects.get(email=email, password=hashed_password)
            # Store user ID and email in session
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email  # Storing user email for later use
            print("Login successful! User ID:", user.id)
            print("Session data after login:", request.session.items())  # Debugging line
            return redirect('index')
        except CustomUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})

    return render(request, 'login.html')








# Add other views as needed

from django.shortcuts import render, redirect
from .models import CustomUser
from config.firebase import db  # Import Firebase

# index_view.py

from django.shortcuts import render
from config.firebase import db  # Importing the db instance from your firebase.py
from .models import CustomUser  # Import your CustomUser model

from django.http import JsonResponse
from django.shortcuts import render
from .models import CustomUser

def index_view(request):
    return render(request, 'index.html')

def get_user_data(request):
    user_info = None
    client_data = None

    if request.session.get('user_id'):
        user_id = request.session['user_id']
        try:
            user_info = CustomUser.objects.get(id=user_id)
            # You can fetch client data here if needed
            # modified_email = user_info.email.replace('@', '_at_').replace('.', '_dot_')
            # client_data_from_db = db.reference("clients").child(modified_email).get()
            # if client_data_from_db is not None:
            #     client_data = client_data_from_db.val()
        except CustomUser.DoesNotExist:
            user_info = None
        except Exception as e:
            print(f"An error occurred: {e}")

    return JsonResponse({
        'user_info': user_info.serialize() if user_info else None,
        'client_data': client_data
    })





def add_client_details(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # Redirect to login if not logged in

    # Retrieve the user details
    user = CustomUser.objects.get(id=user_id)
    email = user.email
    username = user.username

    # Retrieve client data from Firebase if it exists
    modified_email = email.replace('@', '_at_').replace('.', '_dot_')
    client_data = db.child("clients").child(modified_email).get()

    # Initialize form fields with existing client data or empty strings
    name = ''
    city = ''
    two_fa_pass = ''
    groq_api_key = ''
    linkedin = ''

    if client_data.val() is not None:  # Check if client data exists
        client_info = client_data.val()
        name = client_info.get('name', '')
        city = client_info.get('city', '')
        two_fa_pass = client_info.get('two_fa_pass', '')
        groq_api_key = client_info.get('groq_api_key', '')
        linkedin = client_info.get('linkedin', '')

    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        two_fa_pass = request.POST.get('two_fa_pass')
        groq_api_key = request.POST.get('groq_api_key')
        linkedin = request.POST.get('linkedin')

        # Create or update client entry in Firebase
        client_data = {
            "name": name,
            "email": email,
            "city": city,
            "two_fa_pass": two_fa_pass,
            "groq_api_key": groq_api_key,
            "username": username,
            "linkedin": linkedin
        }

        # Push client data to the database
        db.child("clients").child(modified_email).set(client_data)
        return redirect('index')  # Redirect after successful submission

    return render(request, 'add_client.html', {
        'email': email,
        'username': username,
        'name': name,
        'city': city,
        'two_fa_pass': two_fa_pass,
        'groq_api_key': groq_api_key,
        'linkedin': linkedin
    })


def logout_view(request):
    request.session.flush()  # Clear the session data
    return redirect('login')  # Redirect to login page



import chromadb
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")

from django.shortcuts import render, redirect
from django.contrib import messages

import chromadb  # Import your vector store client

# Initialize your vector store client
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")

import chromadb
from django.shortcuts import render, redirect
from django.contrib import messages
import uuid

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
import chromadb

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")

import uuid
from django.shortcuts import redirect, render
from django.contrib import messages
import chromadb

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")

def clear_collection():
    """Clear all documents from the ChromaDB collection."""
    collection.clear()

import uuid
from django.shortcuts import redirect, render
from django.contrib import messages
import chromadb


# Initialize ChromaDB client and collection globally
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")


import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now  # For added_on field
import chromadb

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now  # For added_on field
import chromadb

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient('vectorstore')
collection = chroma_client.get_or_create_collection(name="portfolio")


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserLink

def manage_links_view(request):
    if request.method == 'POST':
        # Handle adding a new link
        if 'job_role' in request.POST and 'url' in request.POST:
            job_role = request.POST.get('job_role')
            url = request.POST.get('url')

            # Create a new UserLink instance and save it
            username = request.session.get('username')  # Get username from session
            email = request.session.get('user_email')   # Get email from session
            
            UserLink.objects.create(username=username, email=email, job_role=job_role, url=url)
            messages.success(request, "Link added successfully!")
        
        # Handle deleting a link
        elif 'delete_link_id' in request.POST:
            link_id = request.POST.get('delete_link_id')
            UserLink.objects.filter(id=link_id).delete()
            messages.success(request, "Link deleted successfully!")

        return redirect('manage_links')

    # Query to get all existing links from the database
    links = UserLink.objects.all()

    return render(request, 'links.html', {'links': links})


import os
import re
import requests
from django.shortcuts import render
from django.http import JsonResponse
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from .models import CustomUser
from config.firebase import db  # Make sure you have your firebase.py imported correctly

def clean_text(text):
    """Cleans the input text by removing HTML tags, URLs, and non-alphanumeric characters."""
    text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s{2,}', ' ', text)  # Remove multiple spaces
    return text.strip()

def extract_jobs(cleaned_text, groq_api_key):
    """Extracts job postings from the cleaned text using the Groq API."""
    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
        """
    )
    
    llm = ChatGroq(
        temperature=0,
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Split the cleaned_text into smaller chunks if it's too long
    max_context_length = 40000  # Adjust based on the model's limitations
    if len(cleaned_text) > max_context_length:
        cleaned_text = cleaned_text[:max_context_length]  # Truncate for the sake of processing

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={"page_data": cleaned_text})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(res.content)
        print(res)
    except OutputParserException as e:
        return {"error": str(e)}

    return res if isinstance(res, list) else [res]

def write_mail(job, custom_prompt):
    """Generates a cold email based on the job description and custom prompt."""
    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        Write a cold email to the hiring manager regarding the job mentioned above. 
        Describe how your skills and experience align with the job requirements. 
        Use the following details to personalize your email: {custom_prompt}
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        """
    )
    
    # Your API key is directly included here
    groq_api_key = os.getenv('GROQ_API_KEY')


    llm = ChatGroq(
        temperature=0,
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"
    )
    
    job_description_with_prompt = job['description']  # Use the job description from extracted job
    chain_email = prompt_email | llm
    res = chain_email.invoke({"job_description": job_description_with_prompt, "custom_prompt": custom_prompt})
    return res.content
def index_view(request):
    """Renders the index page with user and client data."""
    user_info = None
    client_data = None

    if request.method == 'GET' and request.session.get('user_id'):
        user_id = request.session['user_id']
        try:
            user_info = CustomUser.objects.get(id=user_id)
            modified_email = user_info.email.replace('@', '_at_').replace('.', '_dot_')

            # Get client data from Firebase using Pyrebase
            client_data_from_db = db.child('clients').child(modified_email).get()

            if client_data_from_db.val() is not None:
                client_data = client_data_from_db.val()

        except CustomUser.DoesNotExist:
            user_info = None  # Reset user_info if not found

    return render(request, 'index.html', {
        'user_info': user_info,
        'client_data': client_data,
    })



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import requests
from config.firebase import db  # Import your Firebase DB module

import json
from django.http import JsonResponse

def generate_email_view(request):
    """Handles the generation of the email based on job URL and custom prompt."""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            job_url = data.get('job_url')
            custom_prompt = data.get('custom_prompt')

            # Use session data for user information
            user_id = request.session.get('user_id')
            user_email = request.session.get('user_email')

            if user_id and user_email:
                modified_email = user_email.replace('@', '_at_').replace('.', '_dot_')

                # Get client data from Firebase using your firebase.py
                client_data_from_db = db.child('clients').child(modified_email).get()

                if client_data_from_db.val() is not None:
                    client_data = client_data_from_db.val()
                    groq_api_key = client_data.get('groq_api_key')

                    # Print the API key to the terminal for debugging (remove this in production!)
                    print(f"Retrieved Groq API Key: {groq_api_key}")  # Debugging line

                    if not groq_api_key:  # Check if API key is missing
                        return JsonResponse({'error': 'Missing Groq API Key.'}, status=400)

                    # Fetch the job description from the URL
                    response = requests.get(job_url)
                    cleaned_text = clean_text(response.text)

                    # Remove unnecessary whitespaces from cleaned_text
                    cleaned_text = ' '.join(cleaned_text.split())

                    # Extract jobs from the cleaned text
                    jobs = extract_jobs(cleaned_text, groq_api_key)

                    # Generate email for the first job
                    if jobs:
                        first_job = jobs[0]
                        email_content = write_mail(first_job, custom_prompt)

                        return JsonResponse({'generated_email': email_content})

                    return JsonResponse({'error': 'No jobs found.'}, status=404)

            return JsonResponse({'error': 'Invalid user session.'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from django.core.mail import get_connection, EmailMessage
from django.conf import settings

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            # Get the email details from the request body
            data = json.loads(request.body)
            target_email = data.get('target_email')
            email_content = data.get('email_content')
            client_mail = data.get('client_mail')  # Get client mail
            client_2fa = data.get('client_2fa')    # Get client 2FA

            # Replace <br> tags with spaces
            email_content = email_content.replace('<br>', ' ')

            # Split the content into subject and body
            lines = email_content.splitlines()
            subject = lines[0].strip()  # First line as subject
            body = "\n".join(line.strip() for line in lines[1:])  # Join the rest as body

            # Determine the email sender and password
            if client_mail and client_2fa:  # Check if user provided credentials
                email_sender = client_mail
                email_password = client_2fa
            else:
                email_sender = os.getenv('EMAIL_HOST_USER')
                email_password = os.getenv('EMAIL_HOST_PASSWORD')

            # Create the email connection using user-provided or default credentials
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                fail_silently=False,
                username=email_sender,
                password=email_password,
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                use_tls=settings.EMAIL_USE_TLS
            )

            # Create and send the email
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=email_sender,
                to=[target_email],
                connection=connection,
            )
            email.send()

            return JsonResponse({'status': 'success', 'message': 'Email sent successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid request'}, status=400)
