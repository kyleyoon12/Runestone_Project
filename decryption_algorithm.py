from Crypto.Cipher import AES
import hashlib
from binascii import hexlify

# #Type1 dummy = hexadecimal?
# def decryption():
#     key = "0b1e96db05d64ea4" #16 b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'
#     key_byte = key.encode()
#     #key_byte = b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'
#
#     dummy = "102CE7CE4820D545C4F8A09B204463949E91FEDF46C156973A9D8D908B61016D864CBFD1386F45A1A5E77B375216BC2A" #length 96
#     byte_array = bytearray.fromhex(dummy) #bytearray(b'\x10,\xe7\xceH \xd5E\xc4\xf8\xa0\x9b Dc\x94\x9e\x91\xfe\xdfF\xc1V\x97:\x9d\x8d\x90\x8ba\x01m\x86L\xbf\xd18oE\xa1\xa5\xe7{7R\x16\xbc*')
#     dummy_in_bytes = bytes(byte_array) #b'\x10,\xe7\xceH \xd5E\xc4\xf8\xa0\x9b Dc\x94\x9e\x91\xfe\xdfF\xc1V\x97:\x9d\x8d\x90\x8ba\x01m\x86L\xbf\xd18oE\xa1\xa5\xe7{7R\x16\xbc*'
#     print("length_dummy_in_bytes:", len(dummy_in_bytes))
#     print("dummy_in_bytes:", dummy_in_bytes)
#
#     #no padding
#     obj_no_pad = AES.new(key_byte, AES.MODE_ECB)
#     ssm_no_pad = obj_no_pad.decrypt(dummy_in_bytes)
#     print("ssm_no_pad:", ssm_no_pad) #b'CAB3E4C89001E976FB00B23EAF8BC3C08E16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#     #print("byte length:", len(ssm_no_pad))
#
#     #with zero padding
#     dummy_zero_pad = dummy_in_bytes + b"\x00" * 16
#     obj_with_pad = AES.new(key_byte, AES.MODE_ECB)
#     ssm_with_pad = obj_with_pad.decrypt(dummy_zero_pad)
#     print("ssm_with_pad:", ssm_with_pad) #b'CAB3E4C89001E976FB00B23EAF8BC3C08E16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00E\x7f\xde_U\xa5\xa1\x06]\xf8!U\x0e \x1ao'
#     #print("byte length:", len(ssm_with_pad))
#
#     return ssm_with_pad

#Type1 dummy = string
def decryption():
    key = "0b1e96db05d64ea4" #16 b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'
    key_byte = key.encode()
    #key_byte = b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'

    dummy = "102CE7CE4820D545C4F8A09B204463949E91FEDF46C156973A9D8D908B61016D864CBFD1386F45A1A5E77B375216BC2A" #length 96
    dummy_encoded = dummy.encode("UTF-8")
    #print(len(dummy_encoded))

    #no padding
    obj_no_pad = AES.new(key_byte, AES.MODE_ECB)
    ssm_no_pad = obj_no_pad.decrypt(dummy_encoded)
    print("ssm_no_pad:", ssm_no_pad) #b'&k\xd2\x1f\x91+\xe4\x86Q6\xfd7\xbf\xf3\xab\x02i\x89\xd1F\xfbx~i\xe2\xe4\xb0\xb6-\xcd\xe9\x90\xc1J\x9b\xa2\xe9zZ2\xdf\xbc\xd7\xa2{\x0f\x90\xd8\x85\xa5\xac\x1c\xe7\xcc\xd2#Ji\xb6\xa1\xd7\xbe\xaa\x8f\xf3`b\xac\xe8(\xd6\x7f\x03_6\xf3w\xb8KV\xd9\x80oB\xf0uR1n\xd5\xbcq\xf3\n\x8d\x05'
    print("byte length:", len(ssm_no_pad)) #96

    #with zero padding
    dummy_zero_pad = dummy_encoded + b"\x00" * 32
    obj_with_pad = AES.new(key_byte, AES.MODE_ECB)
    ssm_with_pad = obj_with_pad.decrypt(dummy_zero_pad)
    print("ssm_with_pad:", ssm_with_pad) #b'&k\xd2\x1f\x91+\xe4\x86Q6\xfd7\xbf\xf3\xab\x02i\x89\xd1F\xfbx~i\xe2\xe4\xb0\xb6-\xcd\xe9\x90\xc1J\x9b\xa2\xe9zZ2\xdf\xbc\xd7\xa2{\x0f\x90\xd8\x85\xa5\xac\x1c\xe7\xcc\xd2#Ji\xb6\xa1\xd7\xbe\xaa\x8f\xf3`b\xac\xe8(\xd6\x7f\x03_6\xf3w\xb8KV\xd9\x80oB\xf0uR1n\xd5\xbcq\xf3\n\x8d\x05E\x7f\xde_U\xa5\xa1\x06]\xf8!U\x0e \x1aoE\x7f\xde_U\xa5\xa1\x06]\xf8!U\x0e \x1ao'
    print("byte length:", len(ssm_with_pad)) #128

    return ssm_with_pad

#Type4
def file_decryption(ssm_dummy_value):
    print("\n---file decryption---")
    print("ssm_dummy_value:", ssm_dummy_value)
    print("length_ssm_dummy_value:", len(ssm_dummy_value))
    key = hashlib.sha256(ssm_dummy_value).digest()  # b'\x1e(\x1e\x93\xd3\x96\xc6\xc6j\x07CC\xd9\x9c\t\xb9#\xae\x85\xff\x02\x1a\x9f\xe5>\xd9\x95\xf1\xbe\x8a*\xc5'
    #key2 = hashlib.sha256(ssm_dummy_value).hexdigest()  # 1e281e93d396c6c66a074343d99c09b923ae85ff021a9fe53ed995f1be8a2ac5
    #key_byte = bytes.fromhex(key2) #b'\x1e(\x1e\x93\xd3\x96\xc6\xc6j\x07CC\xd9\x9c\t\xb9#\xae\x85\xff\x02\x1a\x9f\xe5>\xd9\x95\xf1\xbe\x8a*\xc5'
    decryption_key = key[0:16]
    #print("decryption key:", decryption_key)
    #print("decryption key:", hexlify(decryption_key))

    with open("../Decrypt/ALARM/alarm.exml", "rb") as file:
    #with open("../Decrypt/Database/logging_all_bluetooth_dictionary", "rb") as file:
        data = file.read()
        iv = data[0x00:0x10]
        cipher_text = data[0x10:]
        obj = AES.new(decryption_key, AES.MODE_CBC, iv)
        plain = obj.decrypt(cipher_text)

    with open("../Decrypt/decrypted.txt", "wb") as f:
        f.write(plain)

def encryption(ssm_dummy_value):
    enc_key = "0b1e96db05d64ea4" #16 b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'
    enc_key_byte = b'\x30\x62\x31\x65\x39\x36\x64\x62\x30\x35\x64\x36\x34\x65\x61\x34'

    enc_obj = AES.new(enc_key_byte, AES.MODE_ECB)
    enc_dummy = enc_obj.encrypt(ssm_dummy_value)
    print(enc_dummy[0:48])
    print(enc_dummy)
    print(enc_dummy.hex())

ssm_dummy_value = decryption()
file_decryption(ssm_dummy_value[0:96])
#encryption(ssm_dummy_value[0:48])





