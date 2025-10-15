import utils

# Returns list with the parts of message converted to binary numbers.
def convertToBinary(message):
    assert (message != "" or message is not None), "Message is empty"

    enc_text = message.encode('utf-8') # Encoding message to UTF-8 format
    binary_parts = [] # Initializing list, where will be contained bit representations of message symbols.

    # Converting encoding symbols to 8-bit binary numbers. 
    for sym in enc_text:
        binary_parts.append(format(sym, "08b"))
    
    return binary_parts

# Returns list containing 512-bit blocks from the binary-parts array.
def getBlocks(bin_pts):
    assert bin_pts, "No binary parts in the container"
    
    msg_len = len(bin_pts) # Message length in bytes.
    len_section = 8 # Bytes for message length section at the end of block.
    msg_bits = msg_len * 8 # Message length in bits. 

    common_bytes = msg_len + len_section # Common amount of bytes of message and length section.
    padding_bytes = 64 - common_bytes % 64 # Length of zero-padding in bytes.
    blocks_count = common_bytes // 64 + 1 # Amount of blocks.

    blocks = [] # Initializing blocks list.

    for i in range(blocks_count):
        currBlock = [b"" for _ in range(64)] # Initializing list of blocks.
        j = 0

        while j < 64:
            # Adding zero-padding and appending binary 
            # original message length in the end of a block.
            if msg_len == 0:
                # Padding with zeros.
                if padding_bytes != 0:
                    currBlock[j] = format(0, "08b")
                    padding_bytes -= 1
                # Appending original message length.
                else:
                    len_section -= 1
                    currBlock[j] = format((msg_bits >> (8 * len_section)) & 0xFF, "08b") # Binary 64-bit number
            # Filling the block with binary numbers 
            # received from message conversion.
            else:
                currBlock[j] = bin_pts[j + i * 64] 
                msg_len -= 1

                # If the message ends, put a '10000000'
                # delimiter byte right after it.
                if msg_len == 0:
                    j += 1
                    currBlock[j] = format(128, "08b")
                    padding_bytes -= 1
            j += 1
        blocks.append(currBlock)
    return blocks

# Returns list containing filled schedule of given block.
def getMessageSchedule(block):
    assert block, "No blocks were found, array is empty"
    schedule = ['' for _ in range(64)] # Initialize schedule list.
    
    # Copying values from block by concatenating quads
    # of 8-bit numbers to first 16 32-bit words. 
    for i in range(0, 64, 4):
        word = ''.join(block[i:i+4])
        schedule[i//4] = word
    
    # Calculating the remaining 48 words with 
    # a specified formula (watch utils.py).
    for i in range(16, 64):
        schedule[i] = utils.calculateNextWord(schedule[i-16],
                                            schedule[i-15],
                                            schedule[i-7], 
                                            schedule[i-2])

    return schedule

# Returns list of updated hash values.
def getHashValues(schedule, baseValues):
    assert schedule, "The schedule is empty"

    # Initialize hash values in the list if it's empty.
    if not baseValues:
        baseValues = utils.initHashValues()

    K_constants = utils.initKconsts() # Initializing list of K-constants (watch utils.py).

    # Initializing list of working variables and
    # updating their values (watch utils.py) in a loop.
    workingVariables = baseValues.copy()
    for i in range(64):
        workingVariables = utils.updateVariables(workingVariables, K_constants[i], schedule[i])
    
    # Updating hash values by summing it with working variables.
    resultHashValues = []
    for i in range(len(workingVariables)):
        sumOfVals = (int(workingVariables[i], 2) + int(baseValues[i], 2)) & 0xFFFFFFFF
        resultHashValues.append(format(sumOfVals, "032b"))

    return resultHashValues

# Returns hexadecimal representation of concatenated final hash values.
def getSHA256(resultValues):
    assert resultValues, "No values were given"

    # Initializing result hash string 
    # and appending converted values to it in a loop.
    hashString = ""
    for byte in resultValues:
        hashString += format(int(byte, 2), "08x")
    
    return hashString