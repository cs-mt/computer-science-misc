from codecs import decode
import struct

def bin_to_float(b, bits):
    if bits == 32: 
        return struct.unpack('!f',struct.pack('!I', int(b, 2)))[0]
    else:
      """ Convert binary string to a float. """
      bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
      return struct.unpack('>d', bf)[0]


def int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.

        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]


def float_to_bin(value, bits):  # For testing.
    if bits == 32:
        return bin(struct.unpack('!I', struct.pack('!f', value))[0])[2:].zfill(32)
    else:
        """ Convert float to 64-bit binary string. """
        [d] = struct.unpack(">Q", struct.pack(">d", value))
        return '{:064b}'.format(d)


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

# The same can be applied to 64 bit floats. 
# 64 bit float has 1 sign bit, 11 exponent bits, and 52 significand bits. 
# The bias for the 64 bit float is 2^(10) - 1 = 1023

print(float_to_bin(12.25, 32))
print(bin_to_float("01000001010001000000000000000000", 32))

# Sometimes, floating point arithmetic isn't 100% accurate. 
# For example, adding 0.1 and 0.2 will yield the result of 0.30000000000000004 
# This is due to the fact that the exact values of 0.2 and 0.1 cannot be stored using the floating point system.

binary = float_to_bin(0.1, 64)
a = bin_to_float(binary, 64)
print("0.1 in binary is {}, which equals to {:.17f}".format(binary, a))

binary = float_to_bin(0.2, 64)
b = bin_to_float(binary, 64)
print("0.2 in binary is {}, which equals to {:.17f}".format(binary, b))

binary = float_to_bin(0.10000000000000001+0.20000000000000001, 64)
sum = bin_to_float(binary, 64)

print("0.10000000000000001+0.20000000000000001 in binary is {}, which equals to {:.17f}".format(binary, sum))
print("Sum: {}".format(a+b))

# Adding the two actual values (0.10000000000000001, 0.20000000000000001), which are 64bit in this situation, gives us the result "0.30000000000000004". The same happens with 32 bit floats too but with a greater error rate.

