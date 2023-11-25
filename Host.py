import tempmail, yowza, random, json
from random_username.generate import generate_username 

def generate_password():
	chars = "abcdefghijklmnopqrstuvwxyz1234567890"
	password = ""
	for i in range(0, 8):
		password += chars[random.randint(0, len(chars) - 1)]
	return password

tm = tempmail.TempMail()
yo = yowza.Yowza()

email = tm.generateEmail()
number = input("Enter a phone number including the + and country code (eg +17815488297): ")
password = generate_password()
referral = input("Enter a referral code (optional): ")
ctx = yo.createAccount(generate_username()[0], number, email, password, referral)
success = yo.verifyOTP(ctx, input("Enter the OTP: "))
if success:
	account_data = {
	"email": email,
	"password": password,
	"number": number,
	"referral": referral
	}

	with open("accounts.json", "r") as f:
		accounts = json.load(f)	
	accounts.append(account_data)
	with open("accounts.json", "w") as f:
		json.dump(accounts, f)