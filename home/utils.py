import requests, docker
from .models import Dockerfiles, Dockerfile_instructions
import os, re
import json
from django.conf import settings
from django.views.decorators.cache import cache_control
import subprocess
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def search_docker_images(purpose):
    response = requests.get(f'https://hub.docker.com/v2/search/repositories/?query={purpose}&page_size=10')
    data = response.json()
    image_names = [result['repo_name'] for result in data['results'][:5]] # Extract the names of the first 5 images

    images = []
    for image_name in image_names:
        if '/' in image_name:
            # Split the image name into namespace and image components
            namespace, image = image_name.split('/')
        else:
            # If the image name doesn't contain a '/', assume it's in the 'library' namespace
            namespace = 'library'
            image = image_name

        # Get the tags for this image
        response = requests.get(f'https://hub.docker.com/v2/repositories/{namespace}/{image}/tags/')
        data = response.json()

        # If the image has tags, append the first one to the name
        if data['results']:
            image_name += ':' + data['results'][0]['name']

        images.append(image_name)

    return images

def generate_dockerfile(purpose):
    # Search for Docker images related to the purpose
    images = search_docker_images(purpose)

    # For simplicity, just use the first image
    base_image = images[0] if images else 'ubuntu'

    dockerfile_content = f'FROM {base_image}\n'
    # Add more Dockerfile instructions here based on your requirements

    return dockerfile_content

def create_dockerfile(request):
  if request.method == 'POST':

    instructions = Dockerfile_instructions.objects.values_list('name', flat=True)
    print(instructions)
        # Map field names to placeholders
    fields = {instruction: instruction.upper() for instruction in instructions}
    # Map field names to placeholders
    # fields = {
    #   'selected_image': 'FROM',
    #   'label': 'LABEL',
    #   'copy': 'COPY',
    #   'add': 'ADD',
    #     'arg': 'ARG',
    #     'cmd': 'CMD',
    #     'entrypoint': 'ENTRYPOINT',
    #     'env': 'ENV',
    #     'expose': 'EXPOSE',
    #     'healthcheck': 'HEALTHCHECK',
    #     'maintainer': 'MAINTAINER',
    #     'onbuild': 'ONBUILD',
    #     'run': 'RUN',
    #     'shell': 'SHELL',
    #     'stopsignal': 'STOPSIGNAL',
    #     'user': 'USER',
    #     'volume': 'VOLUME',
    #     'workdir': 'WORKDIR'
    # }

    # Load the Dockerfile template
    template_path = os.path.join(settings.BASE_DIR, 'home/', 'dockerfile_template.txt')
    with open(template_path, 'r') as file:
      dockerfile = file.read()

    # Replace each placeholder with the corresponding value or an empty string
    for field, placeholder in fields.items():
      print(field)
      value = request.POST.get(field)
      print(value)
      if value:
        dockerfile = dockerfile.replace('{' + placeholder + '}', placeholder + ' ' + value + '\n\n')
      else:
        dockerfile = dockerfile.replace('{' + placeholder + '}', '')

    selected_file_text = 'FROM ' + request.POST.get('selected_image') +'\n'
    dockerfile = selected_file_text + dockerfile
    

    dockerfile = re.sub('\n\s*\n{2,}', '\n\n', dockerfile)

    # Now dockerfile contains the filled in Dockerfile
    return dockerfile
  
def convert_to_windows_path(path):
    # Remove the '/mnt/' prefix and split the path into components
    components = path[5:].split('/')
    # The first component is the drive letter; add ':' to it
    components[0] += ':'
    # Join the components with '\\'
    return '\\\\'.join(components)
  
def lint_dockerfile(dockerfile_content):
    temp_file_path = os.path.join(settings.BASE_DIR, 'home/', 'dockerfile.txt')
    with open(temp_file_path, 'w') as file:
        file.write(dockerfile_content)
    temp_file_path = convert_to_windows_path(temp_file_path)
    print(temp_file_path)

    try:
        hadolint_path = os.path.join(settings.BASE_DIR, 'home/', 'hadolint.exe')
        # Run Hadolint on the temporary file
        result = subprocess.run(
            [hadolint_path, temp_file_path],
            text=True,
            capture_output=True
        )
        
        output = result.stdout
        # Remove file paths and ANSI escape codes
        output = re.sub(r'.*?:\d+ ', '', output)
        output = re.sub(r'\x1b\[.*?m', '', output)
        # Split the output into lines and get the last line
        return {'message': output}
    except subprocess.CalledProcessError as e:
        return {'error': e.stderr}

def build_dockerfile(dockerfile_content):
    client = docker.from_env()
    temp_file_path = os.path.join(settings.BASE_DIR, 'home/', 'Dockerfile')
    directory_file_path = os.path.join(settings.BASE_DIR, 'home/')
    
    with open(temp_file_path, 'w') as file:
        file.write(dockerfile_content)
    
    container = None
    try:
        # Build the Docker image defined by the Dockerfile
        image, build_logs = client.images.build(path=directory_file_path, tag='temp-image', rm=True)
        print(client.images.build(path=directory_file_path, tag='temp-image', rm=True))
        # Convert build logs to string
        build_output = '\n'.join([log.get('stream', '') for log in build_logs])
        
        return {'message': build_output.strip()}  # Return the build output as a string
    except docker.errors.BuildError as e:
        # If the build fails, capture the error message from the logs
        error_message = ''
        for log in e.build_log:
            if 'error' in log:
                error_message += log['error']
            elif 'errorDetail' in log:
                error_message += log['errorDetail']['message']
            else:
                error_message += str(log)
        
        return {'error': error_message.strip()}  # Return the error message as a string except docker.errors.BuildError as e:
        # If the build fails, capture the error message from the logs
        error_message = e.build_log
        return {'message': str(e.build_log)}
    except Exception as e:
        return {'message': str(e)}
    
    import json

import json
import json

def parse_and_format_server_messages(text):
    # Definim un pattern pentru a identifica conținutul mesajului
    pattern_stream = r'\{\'stream\': \'(.*?)\'\}'
    pattern_status = r'\{\'status\': \'(.*?)\',(?:.*?)\}'
    pattern_depr = r'\[DEPRECATION NOTICE\]\': \'(.*?)\'\}'
    pattern_message = r'\{\'message\': \'(.*?)\'\}'
    
    # Folosim re.findall pentru a găsi toate potrivirile cu pattern-urile în text
    matches_stream = re.findall(pattern_stream, text)
    matches_status = re.findall(pattern_status, text)
    matches_depr = re.findall(pattern_depr, text)
    matches_message = re.findall(pattern_message, text)
    
    # Concatenăm mesajele pentru ambele chei
    stream_messages = '\n'.join(matches_stream)
    status_messages = '\n'.join(matches_status)
    depr_messages = '\n'.join(matches_depr)
    message_messages = '\n'.join(matches_message)

    # Înlocuim mesajele originale din text cu cele extrase
    text = re.sub(pattern_stream, stream_messages, text)
    text = re.sub(pattern_status, status_messages, text)
    text = re.sub(pattern_depr, depr_messages, text)
    text = re.sub(pattern_message, message_messages, text)

    # Returnăm textul modificat
    return text

