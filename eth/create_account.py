from src.eth import create_acct

private_key, address = create_acct()

print("Public Key: ", address)
print("Private Key: ", private_key)
