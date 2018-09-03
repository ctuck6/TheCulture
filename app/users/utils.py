import os, random, string
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from flask_login import current_user

def savePicture(form_picture):
	fileName, fileExtension = os.path.splitext(form_picture.filename)

	if "default" not in fileName:
		random_hex = id_generator()
		pictureFilename = random_hex + fileExtension
		picturePath = os.path.join(current_app.root_path, 'static/profilePics', pictureFilename)
		output_size = (125, 125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picturePath)
		if "default" not in current_user.image_file:
			oldPicture = os.path.join(current_app.root_path, "static/profilePics", current_user.image_file)
			os.remove(oldPicture)
	else:
		pictureFilename = fileName + fileExtension

	return pictureFilename

def sendResetEmail(user):
	token = user.get_reset_token()
	message = Message("Password Reset Request", sender = "no_reply@gmail.com", recipients = [user.email])
	message.body = '''To reset your password, visit the following link:
	
{}

If you did not make this request, ignore this email and no changes will be made.'''.format(url_for("users.reset_token", token = token, _external = True))

	mail.send(message)

def id_generator(size = 8, chars = string.ascii_letters + string.digits + string.punctuation):
	return ''.join(random.choice(chars) for i in range(size))