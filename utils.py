from cryptography.fernet import Fernet
import base64

key =  base64.b64encode(b"JBHBwLTKINeza0WKNNjEHQj8RKpWAyBx") #Fernet.generate_key()
fernet = Fernet(key)

class Utils:
    def encryptText(PlainText):
        encMessage = fernet.encrypt(PlainText.encode())
        return encMessage

    def decryptText(EncodedText):
        decMessage = fernet.decrypt(EncodedText).decode()
        return decMessage

