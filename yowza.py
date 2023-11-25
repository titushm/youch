import requests
import time
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import colorama

def log(msg, colour=colorama.Fore.GREEN):
	print(colorama.Fore.WHITE + "[+] " + colour + msg)


class Yowza():
	headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
	otp = None;

	def createAccount(self, username, number, email, password, referral):
		session = requests.Session()
		log("Username: " + username , colorama.Fore.GREEN)
		log("Phone Number: " + number , colorama.Fore.GREEN)
		log("Email: " + email , colorama.Fore.GREEN)
		log("Password: " + password , colorama.Fore.GREEN)
		log("Referral: " + referral , colorama.Fore.GREEN)
		log("Session object generated", colorama.Fore.YELLOW)
		self.headers["User-Agent"] = generate_user_agent()
		response = session.get("https://www.yowza.social/auth/sign_up", headers=self.headers)
		log("Got mastodon session: " + str (response.cookies.get("_mastodon_session")), colorama.Fore.YELLOW)
		soup = BeautifulSoup(response.text, "html.parser")
		authenticity_token = soup.find("input", {"name": "authenticity_token"})["value"]
		log("Got authenticity token: " + authenticity_token, colorama.Fore.GREEN)
		data = {
			"authenticity_token": authenticity_token,
			"user[account_attributes][username]": username,
			"user[phone]": number,
			"user[email]": email,
			"user[password]": password,
			"user[password_confirmation]": password,
			"user[confirm_password]": '',
			"user[invite_code]": referral,
			"accept": '',
			"user[agreement]": "0",
			"user[agreement]": "1",
			"button": ''
		}
		time.sleep(3)
		response = session.post("https://www.yowza.social/auth", headers=self.headers, data=data)
		soup = BeautifulSoup(response.text, "html.parser")
		error_elements = soup.find_all(class_="error")
		for element in error_elements:
			log(element.text, colorama.Fore.RED)
			raise Exception(element.text)
		log("Created account: status_code " + str(response.status_code), colorama.Fore.GREEN)
		soup = BeautifulSoup(response.text, "html.parser")
		authenticity_token_input = soup.find("input", {"name": "authenticity_token"})
		authenticity_token = authenticity_token_input["value"]
		log("Got otp authenticity token: " + authenticity_token, colorama.Fore.GREEN)
		data = {
			"_method": "patch",
			"authenticity_token": authenticity_token,
			"user[phone]": number,
			"button": ''
		}
		log("Requesting OTP ...", colorama.Fore.YELLOW)
		time.sleep(3)
		response = session.get("https://www.yowza.social/auth/resend_code", headers=self.headers, data=data)
		time.sleep(1)
		response = session.get("https://www.yowza.social/auth/resend_code", headers=self.headers, data=data)
		log("Waiting for OTP ...", colorama.Fore.YELLOW)
		return {"session" :session, "authenticity_token": authenticity_token}
		
	
	def verifyOTP(self, ctx, otp):
		session = ctx["session"]
		authenticity_token = ctx["authenticity_token"]

		log("Got otp: " + otp, colorama.Fore.GREEN)
		data = {
			"_method": "patch",
			"authenticity_token": authenticity_token,
			"user[otp]": otp,
			"button": ""
		}
		response = session.post("https://www.yowza.social/auth/verify_otp", headers=self.headers, data=data)
		log("Verified otp: status_code " + str(response.status_code), colorama.Fore.GREEN)
		log("Done", colorama.Fore.GREEN)
		return True