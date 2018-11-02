import os, string
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from flask_login import current_user


def savePicture(form_picture, oldPicture):
	fileName, fileExtension = os.path.splitext(form_picture.filename)

	if "default" not in fileName:
		random_hex = os.urandom(4).encode('hex')
		pictureFilename = random_hex + fileExtension
		picturePath = os.path.join(current_app.root_path, 'static/profilePics', pictureFilename)
		output_size = (125, 125)
		image = Image.open(form_picture)
		image.thumbnail(output_size)
		image.save(picturePath)
	else:
		pictureFilename = fileName + fileExtension

	if "default" not in str(oldPicture):
			deletePicture = os.path.join(current_app.root_path, "static/profilePics", oldPicture)
			os.remove(deletePicture)

	return pictureFilename


def sendResetEmail(user):
	token = user.get_reset_token()
	message = Message("Password Reset Request", sender="no_reply@gmail.com", recipients=[user.email])
	message.body = '''To reset your password, visit the following link:

{}

If you did not make this request, ignore this email and no changes will be made. If you believe your account has been compromised, visit www.theculture.com/reset_password.

Do not directly reply to this email, as this mailbox is not monitored.'''.format(url_for("users.reset_token", token=token, _external=True))

	mail.send(message)
