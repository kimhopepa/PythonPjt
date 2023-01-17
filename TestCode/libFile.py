
class FileManager :
    def __init__(self):
        print("FileManager.__init__()")

    def readCSV(self, path):
        try:
            print("FileManager.readCSV() ")
        except Exception as e:
            print("Exception : FileManager.readCSV()", e)

    def reatText(self, path):
        try:
            print("FileManager.reatText()")
        except Exception as e:
            print("Exception : FileManager.reatText()", e)