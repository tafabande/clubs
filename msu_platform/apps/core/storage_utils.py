"""
Storage utility functions for file handling.

Provides helper functions for file validation, upload, and URL generation.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from typing import Optional, Tuple
import mimetypes
import magic
import os
import logging

logger = logging.getLogger(__name__)


# Allowed file types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime']
ALLOWED_DOCUMENT_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]

# File size limits (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
MAX_DOCUMENT_SIZE = 20 * 1024 * 1024  # 20 MB


def validate_file_type(file: UploadedFile, allowed_types: list) -> bool:
    """
    Validate file type using magic bytes.

    Args:
        file: Uploaded file
        allowed_types: List of allowed MIME types

    Returns:
        bool: True if valid

    Raises:
        ValidationError: If file type is not allowed
    """
    try:
        # Get MIME type from file content
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)  # Reset file pointer

        if mime not in allowed_types:
            raise ValidationError(
                f"File type '{mime}' is not allowed. Allowed types: {', '.join(allowed_types)}"
            )

        return True
    except Exception as e:
        logger.error(f"File validation error: {e}")
        raise ValidationError(f"Unable to validate file: {str(e)}")


def validate_file_size(file: UploadedFile, max_size: int) -> bool:
    """
    Validate file size.

    Args:
        file: Uploaded file
        max_size: Maximum size in bytes

    Returns:
        bool: True if valid

    Raises:
        ValidationError: If file is too large
    """
    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(f"File size exceeds maximum allowed size of {max_size_mb:.1f} MB")

    return True


def validate_image(file: UploadedFile) -> bool:
    """
    Validate image file.

    Args:
        file: Uploaded image file

    Returns:
        bool: True if valid

    Raises:
        ValidationError: If validation fails
    """
    validate_file_type(file, ALLOWED_IMAGE_TYPES)
    validate_file_size(file, MAX_IMAGE_SIZE)
    return True


def validate_video(file: UploadedFile) -> bool:
    """
    Validate video file.

    Args:
        file: Uploaded video file

    Returns:
        bool: True if valid

    Raises:
        ValidationError: If validation fails
    """
    validate_file_type(file, ALLOWED_VIDEO_TYPES)
    validate_file_size(file, MAX_VIDEO_SIZE)
    return True


def validate_document(file: UploadedFile) -> bool:
    """
    Validate document file.

    Args:
        file: Uploaded document file

    Returns:
        bool: True if valid

    Raises:
        ValidationError: If validation fails
    """
    validate_file_type(file, ALLOWED_DOCUMENT_TYPES)
    validate_file_size(file, MAX_DOCUMENT_SIZE)
    return True


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.

    Args:
        filename: Name of the file

    Returns:
        str: File extension (lowercase, without dot)
    """
    return os.path.splitext(filename)[1].lower().lstrip('.')


def get_mime_type(filename: str) -> Optional[str]:
    """
    Get MIME type from filename.

    Args:
        filename: Name of the file

    Returns:
        str: MIME type or None
    """
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type


def generate_upload_path(instance, filename: str, prefix: str = '') -> str:
    """
    Generate upload path for files.

    Organizes files by type and date:
    - posts/images/2024/05/filename.jpg
    - posts/videos/2024/05/filename.mp4

    Args:
        instance: Model instance
        filename: Original filename
        prefix: Path prefix (e.g., 'posts', 'profiles')

    Returns:
        str: Upload path
    """
    from datetime import datetime
    import uuid

    ext = get_file_extension(filename)
    new_filename = f"{uuid.uuid4()}.{ext}"

    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')

    return f"{prefix}/{year}/{month}/{new_filename}"


def get_cdn_url(file_path: str) -> str:
    """
    Get CDN URL for a file.

    Args:
        file_path: File path in storage

    Returns:
        str: Full CDN URL
    """
    if settings.USE_S3 and hasattr(settings, 'AWS_CLOUDFRONT_DOMAIN'):
        return f"https://{settings.AWS_CLOUDFRONT_DOMAIN}/{file_path}"
    else:
        return f"{settings.MEDIA_URL}{file_path}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_video_duration(file_path: str) -> Optional[float]:
    """
    Get video duration in seconds using FFprobe.

    Args:
        file_path: Path to video file

    Returns:
        float: Duration in seconds or None if unavailable
    """
    try:
        import ffmpeg
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        logger.warning(f"Unable to get video duration: {e}")
        return None


def get_video_metadata(file_path: str) -> dict:
    """
    Get video metadata using FFprobe.

    Args:
        file_path: Path to video file

    Returns:
        dict: Video metadata (duration, resolution, codec, etc.)
    """
    try:
        import ffmpeg
        probe = ffmpeg.probe(file_path)

        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
            None
        )

        if not video_stream:
            return {}

        return {
            'duration': float(probe['format'].get('duration', 0)),
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0)),
            'codec': video_stream.get('codec_name', ''),
            'bitrate': int(probe['format'].get('bit_rate', 0)),
            'size': int(probe['format'].get('size', 0)),
        }
    except Exception as e:
        logger.error(f"Unable to get video metadata: {e}")
        return {}


def generate_thumbnail_path(video_path: str) -> str:
    """
    Generate thumbnail path for a video.

    Args:
        video_path: Path to video file

    Returns:
        str: Path for thumbnail
    """
    base_path = os.path.splitext(video_path)[0]
    return f"{base_path}_thumb.jpg"


def is_video_file(filename: str) -> bool:
    """
    Check if file is a video based on extension.

    Args:
        filename: Name of the file

    Returns:
        bool: True if video file
    """
    mime_type = get_mime_type(filename)
    return mime_type in ALLOWED_VIDEO_TYPES if mime_type else False


def is_image_file(filename: str) -> bool:
    """
    Check if file is an image based on extension.

    Args:
        filename: Name of the file

    Returns:
        bool: True if image file
    """
    mime_type = get_mime_type(filename)
    return mime_type in ALLOWED_IMAGE_TYPES if mime_type else False
