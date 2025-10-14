import hashlib

# source message (TODO: make this an input value)
message = "hello world"

# encoding message to bytes
message_to_bytes = message.encode('utf-8')

# encrypting message
message_encrypted = hashlib.sha256(message_to_bytes)

# printing the result
print(f"Encrypted message: {message_encrypted.hexdigest()}")
