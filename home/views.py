from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from .utils import lint_dockerfile, search_docker_images, create_dockerfile
from django.contrib.auth.decorators import login_required
from .models import Dockerfile_explanations
from .models import ImageText, Dockerfile_instructions
import os
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import build_dockerfile, parse_and_format_server_messages
import requests, docker
from docker.errors import APIError
# Create your views here.

def landing(request):

    # Page from the theme 
    return render(request, 'index.html')


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            HttpResponse('Login successful.')
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid username or password.')
    else:
        # Render the login form
        return render(request, 'my_login.html')
    

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['psw']
        #user = User.objects.create_user(username, password, email, first_name=first_name, last_name=last_name)
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        return HttpResponse('Account created successfully.')
    else:
        # Render the sign-up form
        return render(request, 'my_signup.html')

@login_required
def home(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        selected_image = request.POST.get('selected_image')
        copy_path = request.POST.get('copy')
        label = request.POST.get('label')
        add_file = request.POST.get('add')
        arg = request.POST.get('arg')
        cmd = request.POST.get('cmd')
        entrypoint = request.POST.get('entrypoint')
        env = request.POST.get('env')
        expose = request.POST.get('expose')
        healthcheck = request.POST.get('healthcheck')
        maintainer = request.POST.get('maintainer')
        onbuild = request.POST.get('onbuild')
        run = request.POST.get('run')
        shell = request.POST.get('shell')
        stopsignal = request.POST.get('stopsignal')
        user = request.POST.get('user')
        volume = request.POST.get('volume')
        workdir = request.POST.get('workdir')
        action = request.POST.get('action')


        # in aceeasi metoda este si situatia in care se apasa oe search(selected_image nu e selectat) si cand se apasa pe submit
        if action == 'submit' and selected_image:
            # dockerfile_content = generate_dockerfile(selected_image)
            # Do something with dockerfile_content...

            # Open the template file and read its contents
            template_path = os.path.join(settings.BASE_DIR, 'home/', 'dockerfile_template.txt')
            with open(template_path, 'r') as f:
                template = f.read()
                
            images = search_docker_images(purpose)
            # Format the template string with the user's data
#             formatted_template = template.format(
#     username=request.user.username,
#     image_text=selected_image,
#     copy=copy_path,
#     add=add_file,
#     arg=arg,
#     cmd=cmd,
#     entrypoint=entrypoint,
#     env=env,
#     expose=expose,
#     healthcheck=healthcheck,
#     maintainer=maintainer,
#     onbuild=onbuild,
#     run=run,
#     shell=shell,
#     stopsignal=stopsignal,
#     user=user,
#     volume=volume,
#     workdir=workdir,
#     label=label
# )
            
            formatted_template = create_dockerfile(request)
            
            # formatted_template = formatted_template.replace('\n', '<br>')
            # Create a new ImageText and save it to the database
            ImageText.objects.create(user=request.user,purpose = selected_image, text=formatted_template)
        elif action == 'search':
            images = search_docker_images(purpose)
            return render(request, 'home.html', {'images': images, 'instructions': instructions})

    instructions = Dockerfile_instructions.objects.all()
    for instruction in instructions:
        explanation = Dockerfile_explanations.objects.get(instruction=instruction.id)
        instruction.summary_explanation = explanation.summary_explanation
    print(instructions)
    return render(request, 'home.html', {'instructions': instructions})


def get_all_images(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request, or '' if it doesn't exist
    images = search_docker_images(query)
    return JsonResponse({'images': images})

# @login_required
# def create_file(request):
#     if request.method == 'POST':
#         text = request.POST.get('selected_image')
#         ImageText.objects.create(user=request.user, purpose=text, text=text)
#         file_content = request.POST.get('file_content')
#         if file_content:  # Simple validation to check if content is not empty
#             UserFileHistory.objects.create(user=request.user, file=file_content)
#             return redirect('history')
#     return render(request, 'create_file.html')

@login_required
@never_cache
def file_history(request):
    # Get the user's data
    dockerfiles = ImageText.objects.filter(user=request.user)
    image_texts_str = '\n'.join(image_text.text for image_text in dockerfiles)

    # Open the template file and read its contents
    # with open('home/dockerfile_template.txt', 'r') as f:
    #     template = f.read()

    # # Format the template string with the user's data
    # formatted_template = template.format(username=request.user.username, image_texts=image_texts_str)

    # # Write the formatted template string to a file
    # with open('user_data.txt', 'w') as f:
    #     f.write(formatted_template)

    return render(request, 'file_history.html', {'dockerfiles': dockerfiles})

@login_required
def modify_dockerfile(request, file_id=None):
    # your code here...
    user_files = ImageText.objects.filter(user=request.user)
    selected_file = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save':
            print('Save action')
            updated_content = request.POST.get('file-content')
            if file_id:
                # If a file is selected, update the existing file
                selected_file = ImageText.objects.get(id=file_id)
                selected_file.text = updated_content
                selected_file.save()
                print('File updated')
            else:
            # If no file is selected, create a new file
                print('File created')
                selected_file = ImageText.objects.create(user=request.user, text=updated_content)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': 'success', 'error': 'error'})
            return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file})
        elif action == 'build':
            # Get the updated content from the form
            print('Build action')
            updated_content = request.POST.get('file-content')
            build_result = build_dockerfile(updated_content)
            formatted_messages = parse_and_format_server_messages(build_result.get('message', ''))
            error_message = parse_and_format_server_messages(build_result.get('error', ''))
            # print(build_result.get('message', ''), build_result.get('error', ''))
            # print(formatted_messages)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'message': formatted_messages, 'error': error_message})
            # if build_result:
            #     print("here")
            #     raw_messages = build_result.get('error', '')
            #     formatted_messages = parse_and_format_server_messages(raw_messages)
            #     build_message = '\n'.join(formatted_messages)
            #     return render(request, 'write_dockerfile.html', {
            #         'user_files': user_files,
            #         'selected_file': selected_file,
            #         'lint_result': formatted_messages
            #     })
                # Handle the case where the Dockerfile is valid
        elif action == 'check':
            updated_content = request.POST.get('file-content')
            lint_result = lint_dockerfile(updated_content)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(lint_result)
            if lint_result:
                build_message = str(lint_result.get('message', ''))  # Asigură-te că obții mesajul din rezultat
                return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file, 'lint_result': build_message})
            # Handle the case where the Dockerfile is valid
        elif action == 'push':
            # Conectează-te la clientul Docker
            client = docker.from_env()

            # Numele imaginii Docker pe care dorești să o creezi și să o încarci pe DockerHub
            docker_image_name = request.POST.get('docker_name')

            # Calea către Dockerfile în sistemul de fișiere
            dockerfile_path = '/cale/catre/Dockerfile'

            # Construiește imaginea Docker folosind Dockerfile-ul din calea specificată
            image, build_logs = client.images.build(path=dockerfile_path, tag=docker_image_name)

            # Autentifică-te pe DockerHub (înlocuiește 'username' și 'password' cu credențialele tale reale)
            client.login(username='username', password='password')

            # Efectuează push-ul imaginii către DockerHub
            push_logs = client.images.push(docker_image_name, stream=True)

            # Returnează o pagină de succes sau de confirmare

            return render(request, 'dockerfile_push_success.html')


    if file_id:
        selected_file = ImageText.objects.get(id=file_id)
    return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file})

@never_cache
def delete_template(request, image_text_id):
    ImageText.objects.get(id=image_text_id).delete()
    return redirect('history')

@never_cache
def delete_template_editor(request, image_text_id):
    ImageText.objects.get(id=image_text_id).delete()
    return redirect('write_dockerfile')

@require_GET
def search(request):
    image_name = request.GET.get('image_name', '')
    images = search_docker_images(image_name)  # call your function here
    return JsonResponse(images, safe=False)

def open_file(request, file_id):
    # Fetch the file
    file = ImageText.objects.get(id=file_id)
    # Open the file in the editor
    # ...
    return render(request, 'open_file.html', {'file': file})




def dockerfile_push(request):
    if request.method == 'POST':
        dockerfile_content = request.POST.get('file-content')
        print(dockerfile_content)

        temp_file_path = os.path.join(settings.BASE_DIR, 'home/', 'Dockerfile')
        directory_file_path = os.path.join(settings.BASE_DIR, 'home/')
        
        with open(temp_file_path, 'w') as file:
            file.write(dockerfile_content)
        username = request.POST.get('docker_username')
        password = request.POST.get('docker_password')
              
        try:
            client = docker.from_env()
            client.login(username, password)
            # Build and push the Docker image...
            # You'll need to replace 'path/to/dockerfile' and 'myusername/myimage' with your actual values
            image, build_logs = client.images.build(path=directory_file_path, tag=f'{username}/myimage', rm=True)
            push_logs = client.images.push(f'{username}/myimage', stream=True)
            for line in push_logs:
                print(line)
            print("success")
            return JsonResponse({'status': 'success'})  # Return a JSON response for success
        except APIError:
            print("failure")
            return JsonResponse({'status': 'failure', 'error': 'Invalid username or password'})  # Return a JSON response for failure
        except Exception as e:
            print("failure")
            return JsonResponse({'status': 'failure', 'error': str(e)})       
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def docker_login(request):
    if request.method == 'POST':
        username = request.POST.get('docker_username')
        password = request.POST.get('docker_password')

        if username and password:
            client = docker.from_env()
            try:
                client.login(username, password)
                return JsonResponse({'status': 'success'})
            except docker.errors.APIError:
                return JsonResponse({'status': 'failure', 'error': 'Invalid username or password'})

        else:
            return JsonResponse({'status': 'failure', 'error': 'Username and password are required'})
        
import yaml

def convert_to_docker_compose(dockerfiles):
    services = {}
    
    for i, dockerfile in enumerate(dockerfiles):
        service_name = f"service_{i+1}"
        services[service_name] = {
            "build": {
                "context": ".",
                "dockerfile": dockerfile
            },
            "container_name": service_name
        }
    
    docker_compose = {
        "version": "3",
        "services": services
    }
    
    return yaml.dump(docker_compose, default_flow_style=False)

import json
@csrf_exempt
@login_required
def docker_compose(request):
    if request.method == 'POST':
        print("am ajuns")
        dockerfiles = json.loads(request.POST.get('dockerfiles'))
        print(dockerfiles)
        docker_compose_content = convert_to_docker_compose(dockerfiles)
        print(docker_compose_content)

        return JsonResponse({'docker_compose_content': docker_compose_content})

@login_required
def dockerfile_learn(request):
    instructions = Dockerfile_instructions.objects.all()
    for instruction in instructions:
        explanation = Dockerfile_explanations.objects.get(instruction=instruction.id)
        instruction.summary_explanation = explanation.summary_explanation
        instruction.explanation = explanation.explanation
        instruction.options = explanation.options
        instruction.examples = explanation.examples
    return render(request, 'dockerfile_learn.html', {'instructions': instructions})
    
