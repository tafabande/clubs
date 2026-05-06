"""
File upload validators for MSU Platform.

Provides validation for:
- File size limits
- File type restrictions
- Image dimensions
- Malicious content detection
"""
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible
import filetype
import os

# File size limits (in bytes)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 20 * 1024 * 1024  # 20MB

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
ALLOWED_ARCHIVE_EXTENSIONS = ['.zip', '.tar', '.gz']

# Allowed MIME types
ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
]
ALLOWED_DOCUMENT_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
]


@deconstructible
class FileSizeValidator:
    """
    Validator to check file size.

    Usage:
        field = models.FileField(validators=[FileSizeValidator(max_size=5*1024*1024)])
    """

    def __init__(self, max_size=MAX_FILE_SIZE, message=None):
        self.max_size = max_size
        self.message = message or f'File size must not exceed {self.max_size // (1024*1024)}MB'

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(
                self.message,
                code='file_too_large',
                params={'max_size': self.max_size, 'size': value.size}
            )

    def __eq__(self, other):
        return isinstance(other, FileSizeValidator) and self.max_size == other.max_size


@deconstructible
class FileExtensionValidator:
    """
    Validator to check file extension.

    Usage:
        field = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['.pdf', '.docx'])])
    """

    def __init__(self, allowed_extensions, message=None):
        self.allowed_extensions = [ext.lower() for ext in allowed_extensions]
        self.message = message or f'Allowed file types: {", ".join(self.allowed_extensions)}'

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                self.message,
                code='invalid_extension',
                params={'extension': ext, 'allowed': self.allowed_extensions}
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionValidator) and
            self.allowed_extensions == other.allowed_extensions
        )


@deconstructible
class MimeTypeValidator:
    """
    Validator to check MIME type using filetype library.

    Usage:
        field = models.FileField(validators=[MimeTypeValidator(allowed_types=['image/jpeg', 'image/png'])])
    """

    def __init__(self, allowed_types, message=None):
        self.allowed_types = allowed_types
        self.message = message or f'File type not allowed'

    def __call__(self, value):
        try:
            # Read file header to determine MIME type
            kind = filetype.guess(value.read(2048))
            value.seek(0)  # Reset file pointer

            if kind is None:
                # If filetype can't guess, check if it's an image or document we know
                mime = 'application/octet-stream'
            else:
                mime = kind.mime

            if mime not in self.allowed_types:
                raise ValidationError(
                    self.message,
                    code='invalid_mime_type',
                    params={'mime_type': mime, 'allowed': self.allowed_types}
                )
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(
                'Could not determine file type',
                code='mime_detection_failed'
            )

    def __eq__(self, other):
        return (
            isinstance(other, MimeTypeValidator) and
            self.allowed_types == other.allowed_types
        )


@deconstructible
class ImageDimensionValidator:
    """
    Validator to check image dimensions.

    Usage:
        field = models.ImageField(validators=[ImageDimensionValidator(
            min_width=100, min_height=100, max_width=4000, max_height=4000
        )])
    """

    def __init__(self, min_width=None, min_height=None, max_width=None, max_height=None, message=None):
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.message = message

    def __call__(self, value):
        width, height = get_image_dimensions(value)

        if width is None or height is None:
            raise ValidationError('Could not determine image dimensions', code='invalid_image')

        if self.min_width and width < self.min_width:
            raise ValidationError(
                self.message or f'Image width must be at least {self.min_width}px',
                code='image_width_too_small',
                params={'width': width, 'min_width': self.min_width}
            )

        if self.min_height and height < self.min_height:
            raise ValidationError(
                self.message or f'Image height must be at least {self.min_height}px',
                code='image_height_too_small',
                params={'height': height, 'min_height': self.min_height}
            )

        if self.max_width and width > self.max_width:
            raise ValidationError(
                self.message or f'Image width must not exceed {self.max_width}px',
                code='image_width_too_large',
                params={'width': width, 'max_width': self.max_width}
            )

        if self.max_height and height > self.max_height:
            raise ValidationError(
                self.message or f'Image height must not exceed {self.max_height}px',
                code='image_height_too_large',
                params={'height': height, 'max_height': self.max_height}
            )

    def __eq__(self, other):
        return (
            isinstance(other, ImageDimensionValidator) and
            self.min_width == other.min_width and
            self.min_height == other.min_height and
            self.max_width == other.max_width and
            self.max_height == other.max_height
        )


def validate_image_file(value):
    """
    Combined validator for image files.

    Checks:
    - File size (max 5MB)
    - File extension (.jpg, .jpeg, .png, .gif, .webp)
    - MIME type
    - Image dimensions (max 4000x4000)
    """
    # Size check
    FileSizeValidator(max_size=MAX_IMAGE_SIZE)(value)

    # Extension check
    FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)(value)

    # MIME type check
    MimeTypeValidator(allowed_types=ALLOWED_IMAGE_TYPES)(value)

    # Dimension check
    ImageDimensionValidator(max_width=4000, max_height=4000)(value)


def validate_document_file(value):
    """
    Combined validator for document files.

    Checks:
    - File size (max 20MB)
    - File extension
    - MIME type
    """
    # Size check
    FileSizeValidator(max_size=MAX_DOCUMENT_SIZE)(value)

    # Extension check
    FileExtensionValidator(allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS)(value)

    # MIME type check
    MimeTypeValidator(allowed_types=ALLOWED_DOCUMENT_TYPES)(value)


def sanitize_filename(filename):
    """
    Sanitize uploaded filename to prevent security issues.

    - Removes path traversal attempts (../, ../../)
    - Removes special characters
    - Limits filename length
    - Preserves file extension
    """
    import re
    from django.utils.text import get_valid_filename

    # Get valid filename (removes path traversal, special chars)
    filename = get_valid_filename(filename)

    # Remove any remaining problematic characters
    filename = re.sub(r'[^\w\s.-]', '', filename)

    # Limit filename length (preserve extension)
    max_length = 100
    name, ext = os.path.splitext(filename)
    if len(filename) > max_length:
        name = name[:max_length - len(ext)]
        filename = f"{name}{ext}"

    return filename


def get_upload_path(instance, filename, folder='uploads'):
    """
    Generate secure upload path for files.

    Structure: {folder}/{year}/{month}/{uuid}_{filename}

    Args:
        instance: Model instance
        filename: Original filename
        folder: Base folder name
    """
    import uuid
    from datetime import datetime

    # Sanitize filename
    filename = sanitize_filename(filename)

    # Generate path with date and UUID
    now = datetime.now()
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"

    return os.path.join(
        folder,
        str(now.year),
        str(now.month).zfill(2),
        unique_filename
    )


def detect_malicious_content(file_obj):
    """
    Basic malicious content detection.

    Checks for:
    - Script tags in files
    - Executable signatures
    - Suspicious patterns

    Returns:
        bool: True if content appears safe, False if potentially malicious
    """
    try:
        # Read first 4KB to check for malicious patterns
        content = file_obj.read(4096)
        file_obj.seek(0)  # Reset pointer

        # Convert to string for pattern checking
        content_str = str(content.lower())

        # Suspicious patterns
        malicious_patterns = [
            b'<script',
            b'javascript:',
            b'eval(',
            b'exec(',
            b'system(',
            b'<?php',
            b'<%',
        ]

        # Check for malicious patterns
        for pattern in malicious_patterns:
            if pattern in content:
                return False

        # Check for executable signatures
        executable_signatures = [
            b'MZ',  # Windows executable
            b'\x7fELF',  # Linux executable
            b'#!',  # Shell script
        ]

        for signature in executable_signatures:
            if content.startswith(signature):
                return False

        return True

    except Exception:
        # If error occurs, be conservative and reject
        return False
