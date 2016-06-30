#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
'''
Created on 2012-11-7

@author: palydawn
'''
import cmath
from BitVector import BitVector

class BloomFilter(object):
    def __init__(self, error_rate, elementNum):
        #璁＄畻鎵�闇�瑕佺殑bit鏁�
        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))

        #鍥涘瓧鑺傚榻�
        self.bit_num = self.align_4byte(self.bit_num.real)

        #鍒嗛厤鍐呭瓨
        self.bit_array = BitVector(size=self.bit_num)

        #璁＄畻hash鍑芥暟涓暟
        self.hash_num = cmath.log(2) * self.bit_num / elementNum

        self.hash_num = self.hash_num.real

        #鍚戜笂鍙栨暣
        self.hash_num = int(self.hash_num) + 1

        #浜х敓hash鍑芥暟绉嶅瓙
        self.hash_seeds = self.generate_hashseeds(self.hash_num)

    def insert_element(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #鍙栫粷瀵瑰��
            hash_val = abs(hash_val)
            #鍙栨ā锛岄槻瓒婄晫
            hash_val = hash_val % self.bit_num
            #璁剧疆鐩稿簲鐨勬瘮鐗逛綅
            self.bit_array[hash_val] = 1

    #妫�鏌ュ厓绱犳槸鍚﹀瓨鍦紝瀛樺湪杩斿洖true锛屽惁鍒欒繑鍥瀎alse 
    def is_element_exist(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #鍙栫粷瀵瑰��
            hash_val = abs(hash_val)
            #鍙栨ā锛岄槻瓒婄晫
            hash_val = hash_val % self.bit_num

            #鏌ョ湅鍊�
            if self.bit_array[hash_val] == 0:
                return False
        return True

    #鍐呭瓨瀵归綈    
    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num

    #浜х敓hash鍑芥暟绉嶅瓙,hash_num涓礌鏁�
    def generate_hashseeds(self, hash_num):
        count = 0
        #杩炵画涓や釜绉嶅瓙鐨勬渶灏忓樊鍊�
        gap = 50
        #鍒濆鍖杊ash绉嶅瓙涓�0
        hash_seeds = []
        for index in range(hash_num):
            hash_seeds.append(0)
        for index in range(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in range(2, max_num):
                if index % num == 0:
                    flag = 0
                    break

            if flag == 1:
                #杩炵画涓や釜hash绉嶅瓙鐨勫樊鍊艰澶ф墠琛�
                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count = count + 1

            if count == hash_num:
                break
        return hash_seeds

    def hash_element(self, element, seed):
        hash_val = 1
        for ch in str(element):
            chval = ord(ch)
            hash_val = hash_val * seed + chval
        return hash_val
if __name__ == '__main__':
    #测试代码
    bf = BloomFilter(0.001, 100000000)
    element = 'palydawn'
    bf.insert_element(element)
    print(bf.is_element_exist('palydawn1'))
