import re, sys
code = open(sys.argv[1] if len(sys.argv) > 1 else 'files/prog.bin', 'rb').read()
mem, k = ({}, 0)

def s32(x):
    return x - 4294967296 if x & 2147483648 else x
ins = []
while k < len(code):
    op = code[k]
    k += 1
    if op == 1:
        ins.append(('PUSH', s32(int.from_bytes(code[k:k + 4], 'little'))))
        k += 4
    else:
        ins.append((op, None))
for i in range(len(ins) - 4):
    (o1, a), (o2, b), (o3, _), (o4, idx), (o5, _) = ins[i:i + 5]
    if o1 == 'PUSH' and o2 == 'PUSH' and (o3 == 7) and (o4 == 'PUSH') and (o5 == 11):
        mem[idx] = (a ^ b) & 255
flag = bytes((mem[i] for i in sorted(mem))).decode()
print(flag)
