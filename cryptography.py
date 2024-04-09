import rsa
import base64

def generate_license(email):
    with open('private_key.pem', 'rb') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())

    signature = rsa.sign(email.encode('utf-8'), privkey, 'SHA-1')
    encrypted_email_readable = base64.b64encode(signature).decode()
    return encrypted_email_readable

def validate_license(email, encrypted_email_readable):
    with open('public_key.pem', 'rb') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read())

    try:
        encrypted_email = base64.b64decode(encrypted_email_readable)
        rsa.verify(email.encode('utf-8'), encrypted_email, pubkey)
        return True
    except:
        return False
    