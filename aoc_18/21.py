_opcodes = {
    'addr': lambda a, b, m: m[a] + m[b],
    'addi': lambda a, b, m: m[a] + b,
    'mulr': lambda a, b, m: m[a] * m[b],
    'muli': lambda a, b, m: m[a] * b,
    'banr': lambda a, b, m: m[a] & m[b],
    'bani': lambda a, b, m: m[a] & b,
    'borr': lambda a, b, m: m[a] | m[b],
    'bori': lambda a, b, m: m[a] | b,
    'setr': lambda a, b, m: m[a],
    'seti': lambda a, b, m: a,
    'gtir': lambda a, b, m: 1 if a > m[b] else 0,
    'gtri': lambda a, b, m: 1 if m[a] > b else 0,
    'gtrr': lambda a, b, m: 1 if m[a] > m[b] else 0,
    'eqir': lambda a, b, m: 1 if a == m[b] else 0,
    'eqri': lambda a, b, m: 1 if m[a] == b else 0,
    'eqrr': lambda a, b, m: 1 if m[a] == m[b] else 0,
}

# Translation and comments on the input
# I really need a disassembler!
m = [0] * 6; ip=0
m[2] = 123
m[2] = m[2] & 456
m[2] = m[2] == 72   # if 123 & 456 != 72 ...
ip = ip + m[2]      # GOTO 5
ip = m[0]           # GOTO 1  // This is the check on and!
m[2] = 0
m[5] = m[2] | 65536     # 0x10000    ~~~~ Comes here after m0 check
m[2] = 2238642          # 0x2228B2
m[3] = m[5] & 255       # 0xFF   ~~~ Comes here after division
m[2] = m[2] + m[3]
m[2] = m[2] & 16777215  # 0xFFFFFF  -- a 16 bit integer is always non-masked
m[2] = m[2] * 65899
m[2] = m[2] & 16777215
m[3] = m[5] < 256       # -> if true, goto 28, otherwise division
ip += m[3]              # GOTO 28
ip += 1                 #
ip = 27                 # [result of 14]
m[3] = 0                # ~~~ Start of division ~~~
m[1] = m[3] + 1
m[1] = m[1] * 256
m[1] = m[1] > m[5]
ip = ip + m[1]
ip = ip + 1
ip = 25                 # GOTO 26
m[3] = m[3] + 1
ip = 17                 # GOTO 18  ~~~ Continue division ~~~
m[5] = m[3]             # This is the interesting result for the division
ip = 7                  # GOTO 8
m[3] = m[2] == m[0]     # ONLY PLACE WHEN m[0] is used!
ip += m[3]
ip = 5                  # GOTO 6


####

m2 = 0
i = 0
results = set()
first_result = None
last_result = None
while True:
    i += 1
    m5 = m2 | 0x10000
    m2 = 0x2228B2
    while True:  # @1
        m3 = m5 & 0xFF  # take only last two bytes of m5
        # calculates m2
        m2 += m3
        m2 &= 0xFFFFFF  # cut m2 to be 16bit
        m2 *= 0x1016B   # multiplies by a constant
        m2 &= 0xFFFFFF  # cut again
        if m5 < 256:
            break  # GOTO @2
        # increments m3 and m5
        m3 = m5 // 0x100  # Lines 17-26
        m5 = m3
        pass  # GOTO @1
    # @2
    if m2 in results:
        break
    results.add(m2)
    if first_result is None:
        first_result = m2
    last_result = m2

print(f'Value for R0 that will break after the _fewest_ instruction is: {first_result}')
print(f'Value for R0 that will break after the _most_ instruction is: {last_result}')
