import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prod_django_project_aws.settings')
application = get_wsgi_application()
