#! /usr/bin/python3
import base64

def main():
    welcome = input("Is Your String Encrypted in Base64? [Y/N]: ")
    while welcome.upper() == "Y":
		
        password = input("What Is The Password You Would Like To Decrypt? ")
        decrypt = base64.b64decode(password)

        print("Decrypted Password: " + str(decrypt))
        welcome = input("Do You Have Another Password To Decrypt? ")

        if welcome.lower() == "yes":
            main()

        else:
            print("Thank You!")
            exit
if __name__ == "__main__":
    main()
