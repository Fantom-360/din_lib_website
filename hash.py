import hashlib

# Input data
data = "Hello, world!"

# Create a SHA-256 hash object
hash_object = hashlib.sha256()

# Update the hash with the bytes of the data
hash_object.update(data.encode())

# Get the hexadecimal representation of the hash
hash_hex = hash_object.hexdigest()

print("SHA-256 Hash:", hash_hex)