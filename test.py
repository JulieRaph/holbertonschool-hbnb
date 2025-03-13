import bcrypt


password = "admin1234"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print("Mot de passe haché : ", hashed_password.decode())




import uuid

# Générer des UUIDs de type UUID4
wifi_id = uuid.uuid4()
pool_id = uuid.uuid4()
ac_id = uuid.uuid4()

# Afficher les UUIDs
print("WiFi UUID:", wifi_id)
print("Swimming Pool UUID:", pool_id)
print("Air Conditioning UUID:", ac_id)