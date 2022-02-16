"""
数据接口：WSI数据
data_define.TXT : 批次，文件夹路径/，标签PN, 文件夹下文件数量， 取用量，训练集用量， 测试集用量
train_pos.TXT: 批次，文件绝对路径
train_neg.TXT: 批次，文件绝对路径
test_pos.TXT:批次，文件绝对路径
test_neg.TXT:批次，文件绝对路径

data/
    data_define.TXT
    train_pos.TXT
    。。。。
"""

import os
import random


def make_data_define(data_path='data/data_define.txt', auto_select_use_by_all=0.5, auto_divide_train_by_all=0.5):
    '''
    data/data_define.TXT : 批次， 文件夹路径/，标签PN
    data/data_define.TXT : 批次， 文件夹路径/，标签PN, 文件夹下文件数量，取用量，训练集用量， 测试集用量
    生成data_define.TXT
    '''
    support_format = ['jpg', 'png', 'tif']
    with open(data_path, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line_ = lines[i].strip().split(',')

        if len(line_) == 2:
            print('=====================please add label======================')

        elif len(line_) == 3:
            num = 0
            for x in os.listdir(lines[i].split(',')[0].strip()):
                if x.split('.')[-1].strip() in support_format:
                    num += 1
            lines[i] = lines[i].strip() + ',{}'.format(num)

            if auto_select_use_by_all:
                use = int(num * auto_select_use_by_all // 1)
                if auto_divide_train_by_all:
                    num_train = int(use * auto_divide_train_by_all // 1)
                    num_test = use - num_train
                    lines[i] = lines[i] + ',{},{},{}'.format(use, num_train, num_test)
                else:
                    lines[i] = lines[i].strip() + ',{}'.format(use)

            lines = [x + '\n' for x in lines]

        elif len(line_) == 4:
            num = int(line_[-1])
            if auto_select_use_by_all:
                use = int(num * auto_select_use_by_all // 1)
                if auto_divide_train_by_all:
                    num_train = int(use * auto_divide_train_by_all // 1)
                    num_test = use - num_train
                    lines[i] = lines[i] + ',{},{},{}'.format(use, num_train, num_test)
                else:
                    lines[i] = lines[i].strip() + ',{}'.format(use)

            lines = [x + '\n' for x in lines]

        elif len(line_) == 5:
            use = int(line_[-1])
            if auto_divide_train_by_all:
                num_train = int(use * auto_divide_train_by_all // 1)
                num_test = use - num_train
                lines[i] = lines[i].strip() + ',{},{}'.format(num_train, num_test)

            lines = [x + '\n' for x in lines]

        elif len(line_) == 7:
            pass

    with open(data_path, 'w') as f:
        f.writelines(lines)


def make_data(data_path='data/data_define.txt'):
    '''
    data/data_define.TXT : 批次， 文件夹路径/，标签, 文件夹下文件数量，取用量，训练集用量， 测试集用量
    train_pos.TXT: 批次，文件绝对路径
    train_neg.TXT: 批次，文件绝对路径
    test_pos.TXT:批次，文件绝对路径
    test_neg.TXT:批次，文件绝对路径
    '''
    support_format = ['jpg', 'png', 'tif']
    with open(data_path, 'r') as f:
        lines = f.readlines()

    for WSI_dir in lines:
        train_pos = []
        train_neg = []
        test_pos = []
        test_neg = []
        x = WSI_dir.split(',')
        data_ = x[0]
        WSIs = [os.path.join(x[1].strip(), x_) for x_ in os.listdir(x[1].strip()) if x_.split('.')[-1].strip() in support_format]
        random.shuffle(WSIs)

        if x[2] == 'P':
            num_train = int(x[-2])
            num_test = int(x[-1])
            train_pos += WSIs[:num_train]
            test_pos += WSIs[-1*num_test:]

        elif x[2] == 'N':
            num_train = int(x[-2])
            num_test = int(x[-1])
            train_neg += WSIs[:num_train]
            test_neg += WSIs[-1*num_test:]

        random.shuffle(test_pos)
        random.shuffle(test_neg)
        random.shuffle(train_neg)
        random.shuffle(train_pos)

        with open(data_path.split('/')[0] + '/train_pos.txt', 'a') as f:
            f.writelines([data_ + ',' + x + '\n' for x in train_pos])
        with open(data_path.split('/')[0] + '/test_pos.txt', 'a') as f:
            f.writelines([data_ + ',' + x + '\n' for x in test_pos])
        with open(data_path.split('/')[0] + '/train_neg.txt', 'a') as f:
            f.writelines([data_ + ',' + x + '\n' for x in train_neg])
        with open(data_path.split('/')[0] + '/test_neg.txt', 'a') as f:
            f.writelines([data_ + ',' + x + '\n' for x in test_neg])

        print('==============size of data {}================='.format(data_))
        print('pos_train{}, pos_test{}, neg_train{}, neg_test{}'.format(len(train_pos), len(test_pos), len(train_neg), len(test_neg)))

