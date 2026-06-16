#!/usr/bin/env python
"""
Generate a secure Django secret key and update .env file.
Run: python generate_secret_key.py
"""
import os
from pathlib import Path

try:
    from django.core.management.utils import get_random_secret_key
except ImportError:
    print("Django not installed. Install requirements first: pip install -r requirements.txt")
    exit(1)

def main():
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    # Check if .env exists
    if not env_file.exists():
        if env_example.exists():
            # Copy from example
            env_file.write_text(env_example.read_text())
            print(f"Created {env_file} from {env_example}")
        else:
            print(f"Error: {env_example} not found")
            exit(1)
    
    # Generate secret key
    secret_key = get_random_secret_key()
    
    # Read current .env
    env_content = env_file.read_text()
    
    # Replace placeholder
    updated = env_content.replace(
        'DJANGO_SECRET_KEY=your-secret-key-here-replace-with-output-from-command-above',
        f'DJANGO_SECRET_KEY={secret_key}'
    )
    
    # Also handle older placeholder format
    updated = updated.replace(
        'DJANGO_SECRET_KEY=replace-this-with-a-secure-key',
        f'DJANGO_SECRET_KEY={secret_key}'
    )
    
    # Write back
    env_file.write_text(updated)
    
    print(f"✓ Secret key generated and saved to {env_file}")
    print(f"\nGenerated key: {secret_key}")

if __name__ == '__main__':
    main()
