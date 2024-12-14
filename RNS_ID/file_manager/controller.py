from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(file_content: bytes) -> (bytes, str):
    """Encrypts the file content and returns the encrypted data and the encryption key."""
    # Generate a random key and IV (initialization vector)
    key = os.urandom(32)  # AES-256 requires a 32-byte key
    iv = os.urandom(16)   # AES block size is 16 bytes

    # Create a cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the file content
    encrypted_content = encryptor.update(file_content) + encryptor.finalize()

    # Return encrypted content and the key (you'll need the key for decryption)
    return encrypted_content, key.hex()  # Convert key to hex for storage

import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_content: bytes, bucket_name: str, filename: str) -> str:
    """Uploads the encrypted file to S3 and returns the S3 URL."""
    s3_client = boto3.client('s3')

    try:
        # Upload the file to the specified S3 bucket
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=file_content,
            ContentType="application/octet-stream"  # Specify the file content type
        )
        return f"s3://{bucket_name}/{filename}"
    except NoCredentialsError:
        raise Exception("Credentials not available")