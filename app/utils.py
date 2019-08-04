import os, random
from os import listdir
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from app.config import Config
import boto3

s3 = boto3.client(
	"s3",
	aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
	aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)

def _delete_file(picture_path):
	os.remove(picture_path)

def generate_header_picture():
	path = "app/static/headerPics"
	pictures = [pic for pic in listdir(path) if "picture" in pic]
	return pictures[random.randint(0, len(pictures) - 1)]

def remove_from_s3(file, folder, bucket_name):
	try:
		s3.delete_object(Bucket=bucket_name, Key="{}/{}".format(folder, file))
	except Exception as e:
		raise e

def _resize_picture(form_picture, size):
	picture_path = os.path.join(current_app.root_path, 'static/profilePics', form_picture.filename)
	output_size = (size, size)
	thumbnail_image = Image.open(form_picture)
	thumbnail_image = thumbnail_image.resize(output_size)
	thumbnail_image.save(picture_path)

	return picture_path

def send_reset_email(user):
	token = user.get_reset_token()
	message = Message("Password Reset Request", sender=Config.THECULTURE_EMAIL, recipients=[user.email])
	message.body = '''To reset your password, visit the following link:

{}

If you did not make this request, ignore this email and no changes will be made.

If you believe your account has been compromised, visit {}.

Do not directly reply to this email, as this mailbox is not monitored.

'''.format(url_for("users.reset_token", token=token, _external=True), url_for("users.reset_request"))

	mail.send(message)

def upload_to_s3(username, file, folder, bucket_name, size):
	from werkzeug.datastructures import FileStorage

	try:
		_, file_extension = os.path.splitext(file.filename)
		picture_filename = username + "_profile_pic" + file_extension
		key = "{}/{}".format(folder, picture_filename)
		picture_path = _resize_picture(file, size)
		with open(picture_path, 'rb') as temp_file:
			new_file = FileStorage(temp_file)
			s3.upload_fileobj(new_file, bucket_name, key, ExtraArgs={"ACL": "public-read"})
		_delete_file(picture_path)

	except Exception as e:
		raise e

	location = s3.get_bucket_location(Bucket=bucket_name)
	return "https://s3-{}.amazonaws.com/{}/{}".format(location["LocationConstraint"], bucket_name, key)
