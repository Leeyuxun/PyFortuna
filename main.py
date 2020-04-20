# -*- coding: utf-8 -*

from accumulator import Accumulator
from seedcreator import SeedCreator

if __name__ == '__main__':
    accumulator = Accumulator()
    try:
        f = open('seedfile', 'rb')
    except :
        with open('/dev/random', 'rb') as random_source:  # Linux内核下的设备文件，记录环境噪声，可用作随机数发生器
            random_source.seek(64, 2)
            seed = random_source.read(64)
            assert len(seed) == 64
    else:
        try:
            seed = f.read(64)
            assert len(seed) == 64
        finally:
            f.close()
    accumulator.generator.reseed(seed)
    SeedCreator().seed_update(accumulator)
    n = 1	# 辅助值
    while n != 0:
        n = input("\n(输入0退出)\n请输入生成的随机数的字节数(n>0): ")
        if n == 0:
            print ("已退出!\n")
            quit()
        elif n < 0:
            print ("输入错误!!!\n")
            quit()
        else:
            print ("\n生成随机数：\n%r" % (accumulator.random_data(int(n))).encode('hex').decode('hex'))
