from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
from .controller import encrypt_file, upload_to_s3
from .models import EncryptedFile

@csrf_exempt
def upload_and_encrypt(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Read the file content
        file_content = file.read()

        # Encrypt the file
        encrypted_content, encryption_key = encrypt_file(file_content)

        # Store the encrypted file to S3
        s3_url = upload_to_s3(encrypted_content, 'lkjhgfbvbfghjm', file.name)

        # Optionally, save metadata to the database
        encrypted_file = EncryptedFile.objects.create(
            original_filename=file.name,
            s3_url=s3_url,
            encryption_key=encryption_key
        )

        return JsonResponse({
            'status': 'success',
            's3_url': s3_url,
            'encryption_key': encryption_key
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
