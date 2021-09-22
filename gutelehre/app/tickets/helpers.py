from flask.ext.mail import Message, Mail

from app.mails import mail

def send_email():
	msg = Message('New Ticket!', sender = 'noreply@gutelehre.de', recipients = ['tickets@gutelehre.de'])
	msg.body = 'New Ticket!'
	mail.send(msg)