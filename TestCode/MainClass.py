
from FileTest.libLog import Logger


class MainClass :

    @staticmethod
    def init(config_path) :
        print("MainClass.init", config_path)
        MainClass.func1()
        MainClass.func2()

    @classmethod
    def func1(self):
        print("func1()")

    @staticmethod
    def func2():
        print("func2()")

if __name__ == '__main__' :
    obj_main = MainClass()
    obj_main.init("path11")
    MainClass.func1()
    MainClass.func2()
    # Logger.init()
    # Logger.info("test")