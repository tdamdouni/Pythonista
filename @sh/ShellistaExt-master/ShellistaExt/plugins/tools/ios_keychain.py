#This is a dummy implementation of keychain which
#does nothing.  Passwords won't be saved if platform
#isn't Pythonista.

def get_password(service, account):
    return None

def set_password(service, account, password):
    pass

def delete_password(service, account):
    pass

def set_master_password():
    pass

def reset_keychain():
    pass

def get_services():
    return []
