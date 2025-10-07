import os
from django.core.management.base import BaseCommand
from django.conf import settings
from OneSas.supabase_storage import SupabaseStorage

class Command(BaseCommand):
    help = 'Upload static files to Supabase storage'
    
    def handle(self, *args, **options):
        storage = SupabaseStorage()
        
        self.stdout.write("Uploading static files to Supabase...")
        
        uploaded_count = 0
        error_count = 0
        
        # Collect static files from all locations
        for static_dir in settings.STATICFILES_DIRS:
            if os.path.exists(static_dir):
                for root, dirs, files in os.walk(static_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, static_dir)
                        supabase_path = f"static/{relative_path}"
                        
                        try:
                            if not storage.exists(supabase_path):
                                with open(file_path, 'rb') as f:
                                    storage.save(supabase_path, f)
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
        
        # Also upload collected static files if they exist
        if os.path.exists(settings.STATIC_ROOT):
            for root, dirs, files in os.walk(settings.STATIC_ROOT):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, settings.STATIC_ROOT)
                    supabase_path = f"static/{relative_path}"
                    
                    try:
                        if not storage.exists(supabase_path):
                            with open(file_path, 'rb') as f:
                                storage.save(supabase_path, f)
                            uploaded_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'✓ Uploaded {supabase_path}')
                            )
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f'✗ Error uploading {supabase_path}: {str(e)}')
                        )
        
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully uploaded {uploaded_count} static files to Supabase storage')
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to upload {error_count} files')
            )