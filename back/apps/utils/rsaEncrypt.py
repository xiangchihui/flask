from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5,PKCS1_OAEP
import base64,sys



def create_rsa_key(passsword='123456'):
    """
    创建RSA密钥,该方法执行一次即可
    步骤说明：
    1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码
    2、生成 1024/2048 位的 RSA 密钥
    3、调用 RSA 密钥实例的 exportKey 方法，传入密码、使用的 PKCS 标准以及加密方案这三个参数。
    4、将私钥写入磁盘的文件。
    5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
    """
    key = RSA.generate(1024)
    encrypted_key = key.exportKey( pkcs=8)
    with open('rsa_private.pem','wb') as f:
        f.write(encrypted_key)
    
    with open("rsa_public.pem",'wb') as f:
        f.write(key.publickey().exportKey())


def decrypt_func(private_path,encrypt_text):
    # 读取密钥
    with open(private_path) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = PKCS1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(encrypt_text),None)
        return text.decode('utf-8')



#加密方法
def encrypt_func(encrypt_text):
    with open('rsa_public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher= PKCS1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(encrypt_text.encode('utf-8')))
        return cipher_text





# if __name__ == "__main__":
#     print(sys._getframe().f_code.co_filename)
#     cipher_text='yqt47MOxTcAqv6sE6c4zb3W5SLm7Tag+GCgjYIEqazyVRAXxJ6oTjIuaMvXmQ4M2fPnW7HS/0MPOkfFW2aTrrw=='
#     print(decrypt_func('apps/utils/clinet_private.pem',cipher_text))
    