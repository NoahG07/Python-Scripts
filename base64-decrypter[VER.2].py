#! /usr/bin/python3
import base64

def main():	
    password = input("What Is The Password You Would Like To Decrypt? ")
    decrypt = base64.b64decode(password)

    print("Decrypted Password: " + str(decrypt))
    welcome = input("Do You Have Another Password To Decrypt? [Yes|No]")

    if welcome.lower() == "yes":
        main()
    else:
        print("Thank You!")
        exit
	
if __name__ == "__main__":
    main()
