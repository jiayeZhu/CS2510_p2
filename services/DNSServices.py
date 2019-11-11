import random

DS_list = ['127.0.0.1:18888', '127.0.0.1:18889', '127.0.0.1:18890']


def getOneDS():
    return random.sample(DS_list, 1)[0]


def setDSList(dsList):
    global DS_list
    DS_list = dsList
