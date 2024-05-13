import requests
import os, re
import json
from django.conf import settings
from django.views.decorators.cache import cache_control


def search_docker_images(query):
    response = requests.get(f'https://hub.docker.com/v2/search/repositories/?query={query}&page_size=10')
    data = response.json()

    # Extract the names of the first 5 images
    image_names = [result['repo_name'] for result in data['results'][:5]]

    images = []
    for image_name in image_names:
        # Check if the image name contains a '/'
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
    # Map field names to placeholders
    fields = {
      'selected_image': 'image_text',
      'label': 'LABEL',
      'copy': 'COPY',
      'add': 'ADD',
        'arg': 'ARG',
        'cmd': 'CMD',
        'entrypoint': 'ENTRYPOINT',
        'env': 'ENV',
        'expose': 'EXPOSE',
        'healthcheck': 'HEALTHCHECK',
        'maintainer': 'MAINTAINER',
        'onbuild': 'ONBUILD',
        'run': 'RUN',
        'shell': 'SHELL',
        'stopsignal': 'STOPSIGNAL',
        'user': 'USER',
        'volume': 'VOLUME',
        'workdir': 'WORKDIR'
    }

    # Load the Dockerfile template
    template_path = os.path.join(settings.BASE_DIR, 'home/', 'dockerfile_template.txt')
    with open(template_path, 'r') as file:
      dockerfile = file.read()

    # Replace each placeholder with the corresponding value or an empty string
    for field, placeholder in fields.items():
      value = request.POST.get(field)
      if value:
        dockerfile = dockerfile.replace('{' + placeholder + '}', placeholder + ' ' + value + '\n\n')
      else:
        dockerfile = dockerfile.replace('{' + placeholder + '}', '')

    dockerfile = re.sub('\n\s*\n{2,}', '\n\n', dockerfile)

    # Now dockerfile contains the filled in Dockerfile
    return dockerfile


