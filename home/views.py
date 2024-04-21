from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import JsonResponse
from .utils import generate_dockerfile, search_docker_images
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
        user = User.objects.create_user(username, password, email, first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        return HttpResponse('Account created successfully.')
    else:
        # Render the sign-up form
        return render(request, 'my_signup.html')
    
def home(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        selected_image = request.POST.get('selected_image')

        if selected_image:
            dockerfile_content = generate_dockerfile(selected_image)
            # Do something with dockerfile_content...
        else:
            images = search_docker_images(purpose)
            return render(request, 'home.html', {'images': images})

    return render(request, 'home.html')

def get_all_images(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request, or '' if it doesn't exist
    images = search_docker_images(query)
    return JsonResponse({'images': images})


    
    
