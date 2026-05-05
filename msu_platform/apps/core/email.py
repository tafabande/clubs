"""
Email utility functions for MSU Platform.

Handles email sending for:
- Email verification
- Password reset
- Organization notifications
- Admin notifications
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_verification_email(user, token):
    """
    Send email verification link to user.

    Args:
        user: User instance
        token: Verification token string
    """
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"

    context = {
        'user': user,
        'verification_url': verification_url,
        'site_name': 'MSU Platform',
    }

    subject = 'Verify Your Email - MSU Platform'
    html_message = render_to_string('emails/verify_email.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return False


def send_password_reset_email(user, token):
    """
    Send password reset link to user.

    Args:
        user: User instance
        token: Password reset token string
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"

    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'MSU Platform',
    }

    subject = 'Reset Your Password - MSU Platform'
    html_message = render_to_string('emails/password_reset.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Password reset email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
        return False


def send_organization_approval_email(organization, creator):
    """
    Send email notification when organization is approved.

    Args:
        organization: Organization instance (Club, Church, etc.)
        creator: User who created the organization
    """
    org_type = organization.__class__.__name__.lower()
    org_url = f"{settings.FRONTEND_URL}/{org_type}s/{organization.id}"

    context = {
        'user': creator,
        'organization': organization,
        'org_type': org_type.title(),
        'org_url': org_url,
        'site_name': 'MSU Platform',
    }

    subject = f'Your {org_type.title()} Has Been Approved - MSU Platform'
    html_message = render_to_string('emails/organization_approved.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[creator.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Organization approval email sent to {creator.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send organization approval email: {str(e)}")
        return False


def send_membership_approved_email(membership, user):
    """
    Send email when user's membership is approved.

    Args:
        membership: Membership instance
        user: User whose membership was approved
    """
    # Get organization based on membership type
    if hasattr(membership, 'club'):
        organization = membership.club
        org_type = 'club'
    elif hasattr(membership, 'church'):
        organization = membership.church
        org_type = 'church'
    elif hasattr(membership, 'sports_team'):
        organization = membership.sports_team
        org_type = 'sports team'
    else:
        return False

    org_url = f"{settings.FRONTEND_URL}/{org_type.replace(' ', '-')}s/{organization.id}"

    context = {
        'user': user,
        'organization': organization,
        'org_type': org_type.title(),
        'org_url': org_url,
        'site_name': 'MSU Platform',
    }

    subject = f'Membership Approved: {organization.name}'
    html_message = render_to_string('emails/membership_approved.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Membership approval email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send membership approval email: {str(e)}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to newly registered user.

    Args:
        user: User instance
    """
    context = {
        'user': user,
        'login_url': f"{settings.FRONTEND_URL}/login",
        'site_name': 'MSU Platform',
    }

    subject = 'Welcome to MSU Platform!'
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def send_admin_notification(subject, message, recipient_emails=None):
    """
    Send notification email to administrators.

    Args:
        subject: Email subject
        message: Email message
        recipient_emails: List of admin emails (defaults to ADMIN_EMAIL from settings)
    """
    if recipient_emails is None:
        recipient_emails = [settings.ADMIN_EMAIL]

    try:
        send_mail(
            subject=f'[MSU Platform Admin] {subject}',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        logger.info(f"Admin notification sent: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send admin notification: {str(e)}")
        return False
