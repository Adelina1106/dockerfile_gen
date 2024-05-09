from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from .utils import generate_dockerfile, search_docker_images
from django.contrib.auth.decorators import login_required
from .models import UserFileHistory
from .models import ImageText
import os
from django.conf import settings
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


        # in aceeasi metoda este si situatia in care se apasa oe search(selected_image nu e selectat) si cand se apasa pe submit
        if selected_image:
            dockerfile_content = generate_dockerfile(selected_image)
            # Do something with dockerfile_content...

            # Open the template file and read its contents
            template_path = os.path.join(settings.BASE_DIR, 'home/', 'dockerfile_template.txt')
            with open(template_path, 'r') as f:
                template = f.read()
                

            # Format the template string with the user's data
            formatted_template = template.format(
    username=request.user.username,
    image_texts=selected_image,
    copy=copy_path,
    add=add_file,
    arg=arg,
    cmd=cmd,
    entrypoint=entrypoint,
    env=env,
    expose=expose,
    healthcheck=healthcheck,
    maintainer=maintainer,
    onbuild=onbuild,
    run=run,
    shell=shell,
    stopsignal=stopsignal,
    user=user,
    volume=volume,
    workdir=workdir,
    label=label
)
            
            formatted_template = formatted_template.replace('\n', '<br>')

            # Create a new ImageText and save it to the database
            ImageText.objects.create(user=request.user, text=formatted_template)
        else:
            images = search_docker_images(purpose)
            return render(request, 'home.html', {'images': images})

    return render(request, 'home.html')

def get_all_images(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request, or '' if it doesn't exist
    images = search_docker_images(query)
    return JsonResponse({'images': images})

@login_required
def create_file(request):
    if request.method == 'POST':
        text = request.POST.get('selected_image')
        ImageText.objects.create(user=request.user, text=text)
        file_content = request.POST.get('file_content')
        if file_content:  # Simple validation to check if content is not empty
            UserFileHistory.objects.create(user=request.user, file=file_content)
            return redirect('file_history')
    return render(request, 'create_file.html')

@login_required
def file_history(request):
    # Get the user's data
    image_texts = ImageText.objects.filter(user=request.user)
    image_texts_str = '\n'.join(image_text.text for image_text in image_texts)

    # Open the template file and read its contents
    # with open('home/dockerfile_template.txt', 'r') as f:
    #     template = f.read()

    # # Format the template string with the user's data
    # formatted_template = template.format(username=request.user.username, image_texts=image_texts_str)

    # # Write the formatted template string to a file
    # with open('user_data.txt', 'w') as f:
    #     f.write(formatted_template)

    return render(request, 'file_history.html', {'image_texts': image_texts})

    
    
