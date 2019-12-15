from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request

def crawler(url):
	html = ""
	receive = requests.get(url)
	if receive.status_code == 200:
		html = receive.text

	soup = BeautifulSoup(html, 'html.parser')
	interest = soup.find("ol", {"class":"wordlist notesView"}).find_all("a")
	return_list = []
	for i in interest:
		converted = str(i)
		return_list.append(converted[converted.index(">")+1:-4])
	return return_list

def papago(msg, reverse=False):
	client_id = "Jla6vYutR83S4LVVoSDi"
	client_secret = "hwSYhBaw4F"
	encText = urllib.parse.quote(msg)
	url = "https://openapi.naver.com/v1/papago/n2mt"
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	if not reverse:
		data = "source=en&target=ko&text=" + encText
	else:
		data = "source=ko&target=en&text=" + encText
	response = urllib.request.urlopen(request, data=data.encode("utf-8"))
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read()
		response_body = response_body.decode('utf-8')
		ind = response_body.index("translatedText") + 17
		return response_body[ind:-4]
	else:
		return "Error Code:" + rescode