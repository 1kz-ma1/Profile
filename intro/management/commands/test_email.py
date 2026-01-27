from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test email sending configuration'

    def handle(self, *args, **options):
        self.stdout.write("Testing email configuration...")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

        if not settings.EMAIL_HOST_USER:
            self.stdout.write(self.style.ERROR("ERROR: EMAIL_HOST_USER is not set"))
            return

        try:
            send_mail(
                subject="Test Email from Portfolio Site",
                message="This is a test email to verify SMTP configuration.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("✅ Email sent successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Email sending failed: {type(e).__name__}: {str(e)}"))
            logger.exception("Email test failed")
