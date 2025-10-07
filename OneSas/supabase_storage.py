import os
import uuid
import requests
from django.core.files.storage import Storage
from django.core.files.base import File
from django.utils.deconstruct import deconstructible
import urllib.parse
from io import BytesIO

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.bucket_name = 'one-sas'
        self.supabase_url = os.getenv('SUPABASE_URL').rstrip('/')
        self.service_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.service_key:
            raise ValueError("Supabase URL and Service Key must be set in environment variables")
    
    def _normalize_path(self, name):
        """Convert Windows backslashes to forward slashes for Supabase"""
        return name.replace('\\', '/')
    
    def _get_headers(self, content_type='application/octet-stream'):
        return {
            'Authorization': f'Bearer {self.service_key}',
            'Content-Type': content_type
        }
    
    def _add_media_prefix(self, name):
        """Add media/ prefix if not already present and not a static file"""
        if name.startswith(('media/', 'static/')):
            return name
        if not name.startswith('media/'):
            return f"media/{name}"
        return name
    
    def get_valid_name(self, name):
        """
        Return a filename that's suitable for Supabase storage.
        """
        # Get the file extension and name
        base_name, ext = os.path.splitext(name)
        
        # Generate a unique filename to avoid conflicts
        unique_id = uuid.uuid4().hex[:8]
        new_name = f"{base_name}_{unique_id}{ext}"
        
        return new_name
    
    def _open(self, name, mode='rb'):
        try:
            name = self._add_media_prefix(name)
            normalized_name = self._normalize_path(name)
            url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{normalized_name}"
            response = requests.get(url)
            response.raise_for_status()
            return File(BytesIO(response.content), name=name)
        except Exception as e:
            if mode == 'rb':
                raise FileNotFoundError(f"File {name} not found in Supabase storage: {str(e)}")
            return File(BytesIO(), name=name)
    
    def _save(self, name, content):
        try:
            # Generate a unique name to avoid conflicts
            name = self.get_valid_name(name)
            name = self._add_media_prefix(name)
            normalized_name = self._normalize_path(name)
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{normalized_name}"
            
            # Ensure we're at the beginning of the file
            if hasattr(content, 'seek') and hasattr(content, 'tell'):
                if content.tell() > 0:
                    content.seek(0)
            
            file_content = content.read()
            
            # Determine content type
            content_type = getattr(content, 'content_type', 'application/octet-stream')
            if hasattr(content, 'name'):
                filename = content.name.lower()
                if filename.endswith(('.jpg', '.jpeg')):
                    content_type = 'image/jpeg'
                elif filename.endswith('.png'):
                    content_type = 'image/png'
                elif filename.endswith('.gif'):
                    content_type = 'image/gif'
                elif filename.endswith('.webp'):
                    content_type = 'image/webp'
            
            headers = self._get_headers(content_type)
            response = requests.post(url, headers=headers, data=file_content)
            
            if response.status_code not in [200, 201, 204]:
                # Improved error handling
                try:
                    # Try to parse as JSON first
                    error_data = response.json()
                    if isinstance(error_data, dict):
                        error_msg = error_data.get('error', {}).get('message', str(error_data))
                    else:
                        error_msg = str(error_data)
                except (ValueError, AttributeError):
                    # If JSON parsing fails, use the raw text
                    error_msg = response.text if response.text else 'Unknown error'
                
                raise Exception(f"Supabase API error {response.status_code}: {error_msg}")
            
            return name
        except Exception as e:
            raise IOError(f"Error saving file {name} to Supabase storage: {str(e)}")
    
    def delete(self, name):
        try:
            name = self._add_media_prefix(name)
            normalized_name = self._normalize_path(name)
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{normalized_name}"
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
        except Exception as e:
            raise IOError(f"Error deleting file {name} from Supabase storage: {str(e)}")
    
    def exists(self, name):
        try:
            name = self._add_media_prefix(name)
            normalized_name = self._normalize_path(name)
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{normalized_name}"
            response = requests.head(url, headers=self._get_headers())
            return response.status_code == 200
        except:
            return False
    
    def url(self, name):
        name = self._add_media_prefix(name)
        normalized_name = self._normalize_path(name)
        encoded_name = urllib.parse.quote(normalized_name)
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{encoded_name}"
    
    def size(self, name):
        try:
            name = self._add_media_prefix(name)
            normalized_name = self._normalize_path(name)
            url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{normalized_name}"
            response = requests.head(url, headers=self._get_headers())
            if response.status_code == 200:
                return int(response.headers.get('content-length', 0))
            return 0
        except:
            return 0
    
    def get_available_name(self, name, max_length=None):
        return self.get_valid_name(name)
    
    def path(self, name):
        """
        This method is required by Django but not supported in cloud storage.
        """
        raise NotImplementedError("This backend doesn't support absolute paths.")