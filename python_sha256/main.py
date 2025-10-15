from hash_funcs import convertToBinary, getBlocks, getMessageSchedule, getHashValues, getSHA256
from hashlib import sha256

msg = input("Input your message here: ")
toBin = convertToBinary(msg)
msg_blocks = getBlocks(toBin)

values = []
for i in range(len(msg_blocks)):
    msg_schedule = getMessageSchedule(msg_blocks[i])
    values = getHashValues(msg_schedule, values)


print(f"SHA256: {getSHA256(values)}")
print(f"HSHLIB: {sha256(msg.encode()).hexdigest()}")
print(f"SHA256 same as in hashlib: {getSHA256(values) == sha256(msg.encode()).hexdigest()}")
