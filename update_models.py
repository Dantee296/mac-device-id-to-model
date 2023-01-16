import requests
import re
from bs4 import BeautifulSoup

# Set our path to the text file
models_file_path = "./models.txt"
# Empty the file for rewriting
open(models_file_path, 'w').close()
# Open the now empty file
models_file = open(models_file_path, 'a')

device_families = ["https://support.apple.com/en-ca/HT201634", # MacBook Pro
	"https://support.apple.com/en-ca/HT201862", # MacBook Air
	"https://support.apple.com/en-ca/HT201300", # iMac
	"https://support.apple.com/en-ca/HT201894", # Mac mini
	"https://support.apple.com/en-us/HT201608", # MacBook
	"https://support.apple.com/en-us/HT202888", # Mac Pro
	"https://support.apple.com/en-ca/HT213073", # Mac Studio 
]
for familyURL in device_families:
	page = requests.get(familyURL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll(lambda tag:tag.name=="strong" and ("(" in tag.text or "Mac" in tag.text))
	for model in results:
		model_name = str(model).replace('<strong>','').replace('</strong>','').replace('<br/>','').strip()
		section = model.find_parent('p')
    # Model info
		model_identifers = ""
		for line in section:
				if "Model" in line:
						model_identifers = str(line).replace("Model Identifier:",'').replace(", ",' ').replace(", ",' ').replace(";",'').strip()
						break
    # Year info
		year_string = None
		for string in section.strings:
				match = re.search(r'\b\d{4}\b', string)
				if match:
						year_string = match.group() 
    # Print the data
		line = model_name + "|" + model_identifers + "|" + year_string
		print(line)
		models_file.write(line + "\n")

# Close the file
models_file.close()
