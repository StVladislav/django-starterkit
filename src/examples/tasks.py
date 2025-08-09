import time
from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@shared_task(bind=True, max_retries=2)
def celery_task(self, *args, **kwargs):
    """
    Tempalte for basic celery task with retries and countdown.
    Prints only for tests.
    """
    print("Start test celery task")

    out = {
        'status': 'started',
        'details': None,
        'error': None,
        'attempt': self.request.retries,
        'result': None
    }
    
    try:
        print(f"START [{self.request.retries}/{self.max_retries}]: celery task is running.")
        for _ in range(5):
            # 1/0 # Use this for test errors handling
            time.sleep(1)
        out.update({
            'status': 'completed',
            'details': 'Task finished successfully',
            'result': 'your result'
        })

        return out
    
    except Exception as e:
        out.update({
            'status': 'retrying',
            'error': str(e),
            'details': f'Will retry in 5 seconds (attempt {out["attempt"]}/{self.max_retries})'
        })

        if self.request.retries < self.max_retries:
            out['status'] = 'retrying'
            print(f"RETRY [{self.request.retries}/{self.max_retries}]: celery task is retrying in 5 sec.")
            self.retry(exc=e, countdown=5)
        else:
            out.update({
                'status': 'failed',
                'details': 'Max retries exceeded',
                'error': 'MaxRetriesExceededError'
            })
            return out


@shared_task
def celery_cron_task():
    """
    Periodic task as an example
    """
    try:
        result = "Your result here"
        print(result)
        return {
            'status': 'success',
            'result': result,
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
        }


@shared_task
def send_email_notification(subject: str, message: str, recipient_list: list):
    """
    Send simple message to each person from the recipient_list
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_email_html_notification(subject: str, context: dict, recipient_list: list):
    """
    Send html message to each person from the recipient_list

    context: dict with message params
    {
        message: str - main message text
        title: str - title inside message
        year: str - year only for demonstrate
        action_url: str - url for required source
    }

    Usage:

    context = {}
    send_email_html_notification.delay(
        ubject="hello from django-starterkit",
        context={},
        recipient_list=["sv6382@gmail.com"]
    )
    """
    context.setdefault('message', 'Greetings from django-starterkit project. Congratulations, the email messages are being sent successfully.')
    context.setdefault("title", "Nice to meet you")
    context.setdefault("year", "2025")
    context.setdefault("action_url", "https://github.com/StVladislav/django-starterkit")

    html_content = render_to_string('emails/notification.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=context.get("message"),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
