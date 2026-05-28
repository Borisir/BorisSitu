import os
from pathlib import Path
from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MediaFilesMiddleware:
    """
    Serve media files from /home/situ_data/media/ directory
    This is necessary for Azure App Service where we can't write to wwwroot
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.media_root = Path(settings.MEDIA_ROOT).resolve()
        logger.info(f"MediaFilesMiddleware initialized with MEDIA_ROOT: {self.media_root}")
    
    def __call__(self, request):
        # If request is for media URL, try to serve from media root
        if request.path.startswith(settings.MEDIA_URL):
            # Remove MEDIA_URL prefix to get the file path
            file_path = request.path[len(settings.MEDIA_URL):]
            full_path = (self.media_root / file_path).resolve()
            
            # Check if file exists and prevent directory traversal
            try:
                # Ensure the file is within MEDIA_ROOT
                if str(full_path).startswith(str(self.media_root)) and full_path.is_file():
                    logger.debug(f"Serving media file: {full_path}")
                    try:
                        return FileResponse(open(full_path, 'rb'))
                    except IOError as e:
                        logger.error(f"Error serving file {full_path}: {e}")
                        return HttpResponseNotFound()
                else:
                    logger.warning(f"Attempted access outside MEDIA_ROOT: {full_path}")
                    return HttpResponseNotFound()
            except (ValueError, OSError) as e:
                logger.error(f"Error accessing media file {file_path}: {e}")
                return HttpResponseNotFound()
        
        response = self.get_response(request)
        return response
