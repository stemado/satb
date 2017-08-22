# Create your tasks here
import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from careplus.celery import app
from celery import shared_task


def send_test_email():

	try:
			email = 'stemado@outlook.com'
			subject = 'Test email from Celery'
			content = 'If you are reading this, then celery worked!'
			send_mail(
				subject, 
				content, 
				'no-reply@careplus.com', 
				[email], 
				fail_silently=False
				)
			print('EMAIL SENT!')
	except:
			print('It didn not send, home skillet.')