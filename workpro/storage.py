import os
from django.core.files.storage import Storage
import cloudinary
from cloudinary import uploader
from io import BytesIO


class CloudinaryStorage(Storage):
    """Simple Cloudinary storage backend"""
    
    def __init__(self):
        if all([os.getenv('CLOUDINARY_CLOUD_NAME'), 
                os.getenv('CLOUDINARY_API_KEY'), 
                os.getenv('CLOUDINARY_API_SECRET')]):
            cloudinary.config(
                cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
                api_key=os.getenv('CLOUDINARY_API_KEY'),
                api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            )
    
    def _save(self, name, content):
        """Save file to Cloudinary"""
        try:
            # Generate public_id from filename
            public_id = os.path.splitext(name)[0]
            result = uploader.upload(content, public_id=public_id, folder='blog_images')
            return f"blog_images/{result['public_id']}"
        except Exception as e:
            print(f"Cloudinary upload error: {str(e)}")
            raise IOError(f"Cloudinary upload failed: {str(e)}")
    
    def url(self, name):
        """Get Cloudinary URL"""
        if not name:
            return ''
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
        if not cloud_name:
            return f'/media/{name}'
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/{name}"
    
    def exists(self, name):
        """Simplified exists check"""
        return bool(name)
    
    def delete(self, name):
        """Delete from Cloudinary"""
        try:
            public_id = name.replace('blog_images/', '').split('.')[0]
            uploader.destroy(f"blog_images/{public_id}")
        except:
            pass  # Ignore errors on delete

