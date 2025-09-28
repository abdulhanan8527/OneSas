# OneSas_app/management/commands/upload_media_to_supabase.py
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from OneSas.supabase_storage import SupabaseStorage

class Command(BaseCommand):
    help = 'Upload existing media files to Supabase storage'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--media-root',
            type=str,
            help='Custom media root directory',
        )
    
    def handle(self, *args, **options):
        storage = SupabaseStorage()
        
        # Use custom media root or default
        media_root = options['media_root'] or settings.MEDIA_ROOT
        
        self.stdout.write(f"Looking for media files in: {media_root}")
        
        if not os.path.exists(media_root):
            self.stdout.write(self.style.WARNING(f'Media directory {media_root} does not exist'))
            self.stdout.write(self.style.WARNING('No files to upload.'))
            return
        
        uploaded_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                # Get relative path from media root and add "media/" prefix
                relative_path = os.path.relpath(file_path, media_root)
                supabase_path = f"media/{relative_path}"  # Add media/ prefix here
                
                try:
                    # Check if file already exists in Supabase (with media/ prefix)
                    if not storage.exists(supabase_path):
                        with open(file_path, 'rb') as f:
                            storage.save(supabase_path, f)  # Save with media/ prefix
                        uploaded_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Uploaded {supabase_path}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'⏭️ Skipped {supabase_path} (already exists)')
                        )
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error uploading {supabase_path}: {str(e)}')
                    )
        
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully uploaded {uploaded_count} media files to Supabase storage')
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to upload {error_count} files')
            )