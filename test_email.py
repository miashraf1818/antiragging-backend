import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antiragging.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email():
    try:
        print('📧 Sending test email...')

        send_mail(
            subject='🔥 Test Email from Anti-Ragging Portal',
            message='This is a test email! If you receive this, your email configuration is working! ✅',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['iamkiradathedeath@gmail.com'],  # Send to yourself
            fail_silently=False,
        )

        print('✅ Email sent successfully!')
        print(f'📬 Check {settings.EMAIL_HOST_USER} inbox!')

    except Exception as e:
        print(f'❌ Error sending email: {e}')


if __name__ == '__main__':
    test_email()
