import utils

# Returns an array with the parts of message converted to binary string.
def convertToBinary(message):
    assert (message != "" or message is not None), "Message is empty"

    enc_text = message.encode('utf-8')
    binary_parts = []

    for sym in enc_text:
        binary_parts.append(format(sym, "08b"))
    
    return binary_parts

# Returns 512-bit blocks from the binary-parts array.
def getBlocks(bin_pts):
    assert bin_pts, "No binary parts in the container"
    
    msg_len = len(bin_pts) # message length in bytes
    len_section = 8 # the amount of bytes length section will demand
    msg_bits = msg_len * 8 # message length in bits 

    common_bytes = msg_len + len_section # the common amount of bytes from message and length section
    padding_bytes = 64 - common_bytes % 64 # the amount of bytes for padding with zeros
    blocks_count = common_bytes // 64 + 1 # the amount of blocks

    blocks = []

    for i in range(blocks_count):
        curr_block = [b"" for _ in range(64)] # filling the array with empty values
        j = 0

        while j < 64:
            # filling the block with additional padding and section
            if msg_len == 0:
                # padding
                if padding_bytes != 0:
                    curr_block[j] = format(0, "08b")
                    padding_bytes -= 1
                # length section
                else:
                    len_section -= 1
                    curr_block[j] = format(msg_bits >> (8 * len_section), "08b")
            # filling the block with byte message
            else:
                curr_block[j] = bin_pts[j + i * 64] 
                msg_len -= 1

                # if the message ends, put a 'single 1' byte after it
                if msg_len == 0:
                    j += 1
                    curr_block[j] = format(128, "08b")
                    padding_bytes -= 1
            j += 1
        blocks.append(curr_block)
    return blocks

def getMessageSchedule(block):
    assert block, "No blocks were found, array is empty"
    messages = [format(0, "032b") for _ in range(64)] # fill with 32-bit zeros
    
    for i in range(0, 64, 4):
        word = ''.join(block[i:i+4])
        messages[i//4] = word
    
    for i in range(16, 64):
        messages[i] = utils.calculateNextWord(messages[i-16], messages[i-15], messages[i-7], messages[i-2])

    return messages

def getHashValues(schedule, baseValues):
    assert schedule, "The schedule is empty"

    if not baseValues:
        baseValues = utils.initHashValues()

    K_constants = utils.initKconsts()

    workingVariables = baseValues.copy()
    for i in range(64):
        workingVariables = utils.updateVariables(workingVariables, K_constants[i], schedule[i])
    
    print(workingVariables)
    
    resultHashValues = []
    for i in range(len(workingVariables)):
        sumOfVals = (int(workingVariables[i], 2) + int(baseValues[i], 2)) & 0xFFFFFFFF
        resultHashValues.append(format(sumOfVals, "032b"))

    return resultHashValues

def getSHA256(resultValues):
    assert resultValues, "No values were given"

    hash_string = ""
    for byte in resultValues:
        hash_string += format(int(byte, 2), "08x")
    
    return hash_string