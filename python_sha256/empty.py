from hash_funcs import convertToBinary, getBlocks, getMessageSchedule, getHashValues, getSHA256
import hashlib

msg = input("Input your message here: ")
toBin = convertToBinary(msg)
msg_blocks = getBlocks(toBin)

values = []
for block in msg_blocks:
    msg_schedule = getMessageSchedule(block)
    values = getHashValues(msg_schedule, values)
    print(values)


print(f"SHA256: {getSHA256(values)}")
print(f"HSHLIB: {hashlib.sha256(msg.encode()).hexdigest()}")
print(f"SHA256 same as in hashlib: {getSHA256(values) == hashlib.sha256(msg.encode()).hexdigest()}")



