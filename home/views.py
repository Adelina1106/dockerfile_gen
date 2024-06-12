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
from .models import ImageText, Dockerfile_instructions, Dockerfile_explanations, Dockerfile_templates
import os
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import build_dockerfile, parse_and_format_server_messages
import requests, docker
from docker.errors import APIError
from django.contrib.auth import logout
# Create your views here.

def landing(request):

    # Page from the theme 
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

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
        return render(request, "my_login.html", {'message': 'Account created successfully. Please log in.'})
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
            print(request.POST.get('ADD'))
            
            # formatted_template = formatted_template.replace('\n', '<br>')
            # Create a new ImageText and save it to the database
            ImageText.objects.create(user=request.user,purpose = selected_image, text=formatted_template)
        elif action == 'search':
            images = search_docker_images(purpose)
            print(purpose)
            instructions = Dockerfile_instructions.objects.all()
            for instruction in instructions:
                explanation = Dockerfile_explanations.objects.get(instruction=instruction.id)
                instruction.summary_explanation = explanation.summary_explanation
                instruction.example = explanation.examples.split(', ')[0]
                print(instruction.example)
            return render(request, 'home.html', {'images': images, 'instructions': instructions})
        else:
            instructions = Dockerfile_instructions.objects.all()
            for instruction in instructions:
                explanation = Dockerfile_explanations.objects.get(instruction=instruction.id)
                instruction.summary_explanation = explanation.summary_explanation
                instruction.example = explanation.examples.split(', ')[0]
                print(instruction.example)
            return render(request, 'home.html', {'instructions': instructions})
    instructions = Dockerfile_instructions.objects.all()
    for instruction in instructions:
        explanation = Dockerfile_explanations.objects.get(instruction=instruction.id)
        instruction.summary_explanation = explanation.summary_explanation
        instruction.example = explanation.examples.split(', ')[0]
        print(instruction.example)
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
    templates = Dockerfile_templates.objects.all()
    print(templates)

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
                return JsonResponse({'message': 'Dockerfile saved'})
            return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file, 'templates': templates})
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
                return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file, 'lint_result': build_message, 'templates': templates})
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
        if ImageText.objects.filter(id=file_id).exists():
            selected_file = ImageText.objects.get(id=file_id)
        else :
            ImageText.objects.create(user=request.user, text=Dockerfile_templates.objects.get(id=file_id).text, id=file_id, purpose=Dockerfile_templates.objects.get(id=file_id).template_name)
        selected_file = ImageText.objects.get(id=file_id)
    # templates
    else:
        selected_file = None


    return render(request, 'write_dockerfile.html', {'user_files': user_files, 'selected_file': selected_file, 'templates': templates})

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
        print(username, password)
              
        try:
            client = docker.from_env()
            print("client")
            client.login(username, password)
            print("login")
            # Build and push the Docker image...
            # You'll need to replace 'path/to/dockerfile' and 'myusername/myimage' with your actual values
            image, build_logs = client.images.build(path=directory_file_path, tag=f'{username}/myimage', rm=True)
            print("build_logs")
            push_logs = client.images.push(f'{username}/myimage', stream=True)
            print("push_logs")
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
        options = []
        if explanation.options != 'No options available' and explanation.options != '-' and explanation.options.__contains__(':'):
            option_lines = explanation.options.split('\n')
            for option_line in option_lines:
                option_split = option_line.split(':')
                if len(option_split) > 1:
                    options.append({'name': option_split[0], 'description': option_split[1]})
        else :
            option_lines = explanation.options.split('\n')
            for option_line in option_lines:
                    options.append({'name': option_line, 'description': ''})
        instruction.options = options
        instruction.examples = explanation.examples.split(', ')
    return render(request, 'dockerfile_learn.html', {'instructions': instructions})
    
# views.py
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect, render

@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = request.POST.get('user')
        user = User.objects.get(username=user)
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            # associated_users = User.objects.filter(email=data)
            print(request.POST.get('email'))
            # if associated_users.exists():
                    # for user in associated_users:
            subject = "Password Reset Requested"
            email_template_name = "password_reset_email.txt"
            c = {
            "email": request.POST.get('email'),
            'domain': request.META['HTTP_HOST'],
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
            }
            email_content = render_to_string(email_template_name, c)
            try:
                print(request.POST.get('email'))
                send_mail(subject, email_content, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("password_reset_done_custom")
    # password_reset_form = PasswordResetForm()
    return render(request, 'custom_password_reset.html')



from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
def custom_password_reset(request, uidb64, token):
    if request.method == 'GET':
        return render(request, 'custom_password_reset.html', {'uidb64': uidb64, 'token': token})
    elif request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Decodează uidb64 pentru a obține id-ul utilizatorului
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Verifică tokenul
        if user is not None and default_token_generator.check_token(user, token):
            # Verifică dacă parolele sunt la fel
            if password1 == password2:
                # Setează noua parolă și salvează
                user.set_password(password1)
                user.save()
                # Opoțional: autentifică automat utilizatorul
                # login(request, user)
                return render(request, 'my_login.html', {'message': 'The password has been successfully reset.'})
            else:
                return render(request, 'custom_password_reset.html', {'uidb64': uidb64, 'token': token, 'error_message': 'Parolele nu se potrivesc.'})
        else:
            return render(request, 'custom_password_reset.html', {'uidb64': uidb64, 'token': token, 'error_message': 'Linkul de resetare a parolei este invalid.'})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})

def password_reset_done_custom(request):
    return render(request, 'password_reset_done_custom.html')

def force_text(s):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return s.decode('utf-8')
    elif hasattr(s, '__unicode__'):
        return str(s)
    else:
        return str(s)



from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import redirect

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'

    def get_success_url(self):
        return '/my_custom_page/'  # Înlocuiește cu URL-ul paginii personalizate la care vrei să redirecționezi utilizatorul
