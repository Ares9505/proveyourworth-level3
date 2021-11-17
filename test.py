import requests
import logging
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw


# Download the payload. Sign it with your name.
# Upload the modified image, your code, and your resum�.
# Do it all with code. Curl, Snoopy, Pear, Sockets... all good. Good luck.

def start_session(url):
	session.get(url)

def activate(start_url, activate_url):
	#Getting hash
	request = session.get(start_url)
	content = BeautifulSoup(request.text)
	hash_value = content.find("input")['value']	
	
	#Activating
	session.get(f'{activate_url}={hash_value}')
	return hash_value

def get_image_and_sing_it(url):
	#Get image
	request = session.get(url,stream = True)
	image = request.raw
	image = Image.open(image)	
	
	#Sing image
	image_to_draw = ImageDraw.Draw(image)
	sing = f'Ariel Irigoyen Castro \n devares3108@gmail.com \n Python Developer \n hello :)'
	image_to_draw.text((30,60),sing)
	image.save("image.png", "PNG")

def upload(payload_url):
	payload = session.get(payload_url)
	
	#To see headers
	print(payload.headers)
	
	post_url = payload.headers['X-Post-Back-To']
	
	#Used to test rigth form delivery and files upload 
	# post_url = "https://httpbin.org/post"
	
	data ={
		"name" : "Ariel Irigoyen Castro",
		"email" : "devares3108@gmail.com",
		"aboutme" : "I'm a telecomunication's engineer. Python is my favorite lenguaje but also now about javascript, C/C++ and Matlab. My goal is give solutions to actual society using my litle knowledge. I'm friendly, hard worker and curious, impatient of cumulate new experiences."   
	}

	files = [open("CV.pdf", "rb"),
	 		 open("test.py", "rb"),
	 		 open("image.png", "rb")
	 		 ]

	jfiles ={ 
		"resume" : files[0],
		"code"   : files[1],
 		"image"  : files[2]
	}
	
	request = requests.post(post_url, data = data, files = jfiles)
	map(lambda x: x.close(), files)

	#Saving my request to inspect 
	with open("out.txt", "w") as sfile:
		sfile.write(request.text)

if __name__ == "__main__":
	logging.basicConfig(level= logging.INFO)
	
	#URLs
	start_url = "http://www.proveyourworth.net/level3/start"
	activate_url = "http://www.proveyourworth.net/level3/activate?statefulhash"
	payload_url = "http://www.proveyourworth.net/level3/payload"

	#Creating session
	session = requests.Session()
	
	logging.info("Starting session")
	start_session(start_url)
	logging.info("End session")


	logging.info("Starting getting hash value from activation")
	hash_value = activate(start_url, activate_url)
	logging.info("End Activation")

	logging.info("Saving sing Image")
	get_image_and_sing_it(payload_url)

	logging.info("Uploading data and files")
	upload(payload_url)
	logging.info("All done")

	



	

