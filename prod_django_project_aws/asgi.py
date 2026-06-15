import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prod_django_project_aws.settings')
application = get_asgi_application()
