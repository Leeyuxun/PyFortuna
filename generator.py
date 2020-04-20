# -*- coding: utf-8 -*

from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class Generator:
    block_size = AES.block_size     # 分组数目
    key_size = 32

    def __init__(self):
        self.counter = Counter.new(nbits=self.block_size * 8, initial_value=0, little_endian=True)  #计数器
        self.key = None

    # 重新生成种子
    def reseed(self, seed):
        # seed 种子
        if self.key is None:
            self.key = b'\0' * self.key_size
        self.set_key(SHA256.new(SHA256.new(self.key + seed).digest()).digest())
        self.counter()

    # 生成新的密钥
    def set_key(self, key):
        self.key = key
        self.cipher = AES.new(key, AES.MODE_CTR, counter=self.counter)

    # 分组 生成AES加密数据块
    def generate_blocks(self, n):
        # n 分组数目
        # 伪造16n字节的随机字节字符串
        assert self.key != b''
        result = b''
        for i in range(n):
            result += self.cipher.encrypt(self.counter())
        return result

    # 生成随机数据
    def pseudo_random_data(self, n):
        # n 要生成随机数据的字节数
        # 返回n字节的随机数据
        assert 0 <= n <= 2**20
        result = self.generate_blocks(n // 16 if n % 16 == 0 else (n // 16) + 1)[:n]
        self.key = self.generate_blocks(2)

        return result
