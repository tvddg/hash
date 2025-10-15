from utils import *
from hash_funcs import *

# the problem is that updating variables
# on the 15th round returns incorrect value 
# from Temp1 + Temp2
k = int(b"11000001100110111111000101110100", 2)
w = int(b"00000000000000000001011111101000", 2)

a = int(b"10100000111100110010101010010010", 2)
b = int(b"11111000010110010110110100011000", 2)
c = int(b"00110110000111010111100010011101", 2)
d = int(b"01101101110011100111011001110100", 2)
e = int(b"11100001001010001010110011001110", 2)
f = int(b"01010010001000010001100111010110", 2)
g = int(b"10111111100111010000111111010011", 2)
h = int(b"01011111100101110000111110001011", 2)

s1 = CapsigOne(e)
print(f"sigma1: {s1:032b}\n")

chc = Choice(e, f, g)
print(f"choice: {chc:032b}\n")

tmp1 = Temp1(h, s1, chc, k, w)
print(f"temp1: {tmp1:032b}\n")

s0 = CapsigZero(a)
print(f"sigma0: {s0:032b}\n")

mjrt = Majority(a, b, c)
print(f"majority: {mjrt:032b}\n")

tmp2 = Temp2(s0, mjrt)
print(f"temp2: {tmp2:032b}\n")

tmp_sum = (tmp1 + tmp2) & 0xFFFFFFFF

print(f"tmp1 + tmp2: {tmp_sum:032b}") # print(f"tmp1 + tmp2: {tmp_sum:032b}")

dTMP1_sum = (d + tmp1) & 0xFFFFFFFF

print(f"d + tmp1: {dTMP1_sum:032b}") # print(f"d + tmp1: {dTMP1_sum:032b}")

print(f"k15: {initKconsts()[15]}")

msg = "Лонгрид — это формат длинного, детального текста, который сочетает в себе как письменный материал, так и мультимедийные элементы, такие как фотографии, видео, инфографика и анимация. Его цель — полностью раскрыть тему, поэтому он часто используется для журналистских материалов, расследований, репортажей и биографий, удерживая внимание читателя с помощью структурированного повествования и визуальных дополнений."
toBin = convertToBinary(msg)
msg_blocks = getBlocks(toBin)
print(msg_blocks[12][-4:])

print(f"{int("101111011111101000", 2) & 0xFF:08b}")