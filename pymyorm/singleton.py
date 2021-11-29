
class Singleton(object):
    def __init__(self, cls):
        # print('singleton init')
        self.__cls = cls
        self.__instance = {}

    def __call__(self):
        # print('singleton call')
        if self.__cls not in self.__instance:
            self.__instance[self.__cls] = self.__cls()
        return self.__instance[self.__cls]
