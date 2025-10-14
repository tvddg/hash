from hash_funcs import convertToBinary, getBlocks, getMessageSchedule # type: ignore
'''msg = input("Enter the message: ")
print(msg)'''

msg = "hello world"

toBin = convertToBinary(msg)
msg_blocks = getBlocks(toBin)

print(msg_blocks)

print("Blocks message: ")
for block in msg_blocks:
    for i in range(len(block)):
        print(block[i], end=" ")
        if (i + 1) % 4 == 0:
            print()
    print(f"Amount of elems: {len(block)}")

msg_schedule = getMessageSchedule(msg_blocks)

for i in range(len(msg_schedule)):
    print(f"w{i}    {msg_schedule[i]}")