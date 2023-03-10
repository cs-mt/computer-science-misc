import struct

def float_to_bin(num):
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

# A 32 bit floating point number is stored in the following format in the memory. 

#  32  - 30    24 - 23     1
# SIGN - EXPONENT - MANTISSA

# An example number (12.25) stored in the binary form:

# 0 10000010 10001000000000000000000

# 0 is the sign. If 0, the number is positive, if 1 the number is negative.

# The following 8 bits are the exponent stored as an unsigned integer. 
# In the exponent of floats, there is a bias which is calculated using the 
# formula 2^(k-1) - 1, where k is the number of bits in the exponent.

# This bias is subtracted from the exponent. This practically makes it possible the exponent to have a sign. 
# The bias in this example (32 bits float) will be 2^(8-1) - 1 = 127 

# The following part is the mantissa. The mantissa serves as the significand portion of the scientific notation. 

# The binary mantissa is converted to decimal in the form of 1/2^1 + 0/2^2 + 0/2^3 + .... 0/2^k

# And the decimal after the . is converted to binary mantissa in the form of 1st_digit/10^1 + 2nd_digit/10^2 + 3rd_digit/10^3 + ... + nth_digit/10^n

# So, let's try to convert the example above to a float on paper. 

# The exponent 10000010 equals 130 in the base 10 system. When we subtract 127 we get 3. 

# The mantissa 10001000000000000000000 can be converted to decimal like 1/2 + 0/4 + 0/8 + 0/16 + 1/32 = 0.53125 

# When we add 1 to it, it becomes 1.53125

# The final result is: 2^3 * 1.53125 = 12.25

print(float_to_bin(12.25))
print(bin_to_float("01000001010001000000000000000000"))
