import requests

class TempMail():
	email = ""
	email_token = ""
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
		"Accept": "*/*",
		"Accept-Language": "en-GB,en;q=0.5",
		"Authorization": f"Bearer {email_token}",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-site",
		"Pragma": "no-cache",
		"Cache-Control": "no-cache"
	}
	def getHeaders(self):
		self.headers["Authorization"] = f"Bearer {self.email_token}"
		return self.headers

	def generateEmail(self):
		response = requests.post("https://web2.temp-mail.org/mailbox", headers=self.headers)
		jsonData = response.json()
		if "errorMessage" in jsonData:
			raise Exception("TEMPMAIL ERROR: " + jsonData["errorMessage"])
		self.email = jsonData["mailbox"]
		self.email_token = jsonData["token"]
		return self.email
	
	def getMail(self):
		response = requests.get("https://web2.temp-mail.org/messages", headers=self.getHeaders())
		return response.json()["messages"]