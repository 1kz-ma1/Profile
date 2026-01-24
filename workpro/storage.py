import os
from django.core.files.storage import Storage
import cloudinary
from cloudinary import uploader
import requests
from io import BytesIO


class CloudinaryStorage(Storage):
    """Custom storage backend for Cloudinary"""
    
    def __init__(self):
        if os.getenv('CLOUDINARY_URL'):
            cloudinary.config(
                cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
                api_key=os.getenv('CLOUDINARY_API_KEY'),
                api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            )
    
    def _open(self, name, mode='rb'):
        """Open file from Cloudinary"""
        url = f"https://res.cloudinary.com/{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        raise FileNotFoundError(f"File {name} not found on Cloudinary")
    
    def _save(self, name, content):
        """Save file to Cloudinary"""
        try:
            result = uploader.upload(content, public_id=name.split('.')[0], folder='blog_images')
            return result['public_id'] + '.' + result['format']
        except Exception as e:
            raise IOError(f"Failed to upload to Cloudinary: {str(e)}")
    
    def url(self, name):
        """Get URL of file from Cloudinary"""
        if not name:
            return ''
        return f"https://res.cloudinary.com/{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload/blog_images/{name}"
    
    def exists(self, name):
        """Check if file exists"""
        if not name:
            return False
        try:
            url = self.url(name)
            response = requests.head(url)
            return response.status_code == 200
        except:
            return False
    
    def delete(self, name):
        """Delete file from Cloudinary"""
        try:
            uploader.destroy(f"blog_images/{name.split('.')[0]}")
        except Exception as e:
            raise IOError(f"Failed to delete from Cloudinary: {str(e)}")
