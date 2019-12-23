from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from django.urls import reverse

class Mail:

    @staticmethod
    def get_absolute_url(url):
        if settings.DEBUG:
            return 'http://localhost:8000{}'.format(
                reverse(url)
            )

    @staticmethod    
    def send_complete_orden(orden, user):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('ordenes/mails/complete.html')
        content = template.render({
            'user': user,
            'next_url': Mail.get_absolute_url('ordenes:completadas')
        })

        message = EmailMultiAlternatives(subject,
                                        'Mensaje importate',
                                        settings.EMAIL_HOST_USER,
                                        [user.email])

        message.attach_alternative(content, 'text/html')
        message.send()