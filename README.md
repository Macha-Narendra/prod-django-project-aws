# Advanced Django Web Application

This repository contains a Django-based web application for Admins and Users to register, login, create products, and browse products.

## Features
- User registration and login via UI
- Product listing, creation, detail pages
- Django admin support for Admin users
- Docker and GitHub Actions scaffolding
- Kubernetes / Helm / Terraform / Ansible deployment examples

## Local setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   source venv/bin/activate      # macOS/Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file from `.env.example`:
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # macOS/Linux
   ```
   - Leave `DATABASE_URL` unset for local SQLite.
   - Set `DATABASE_URL` for production PostgreSQL.
4. Run migrations and start dev server:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/`

## Docker

Build and run with:

```bash
docker build -t django-prod-app .
docker run -p 8000:8000 django-prod-app
```

## GitHub Actions

A CI workflow is included in `.github/workflows/ci.yml` and a CD workflow is included in `.github/workflows/cd.yml`.

The CD workflow is designed to build and push a Docker image to AWS ECR and deploy the Helm chart to EKS. It requires the following repository secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REGISTRY`
- `ECR_REPOSITORY`
- `EKS_CLUSTER_NAME`
- `K8S_NAMESPACE`

## Deployments

- `k8s/` contains sample Kubernetes manifests
- `helm/` contains a Helm chart skeleton
- `terraform/` contains AWS infrastructure scaffolding
- `ansible/` contains a sample playbook

## Next steps

- Add AWS EKS cluster via Terraform
- Use Argo CD for GitOps deployment
- Configure Prometheus and Grafana for metrics
- Harden `settings.py` for production
