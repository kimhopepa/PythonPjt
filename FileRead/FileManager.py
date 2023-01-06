
import csv

class FileManager :
    def __init__(self):
        print("FileManager.__init__()")

    def readCSV(self, path):
        file = open(path, 'r' , encoding='utf-8')
        self.csv_reader_list = csv.reader(file)



    def initialize(self):
        try:
            print("1. CrawlClass().initialize : webdriver.Chrome() ")
        except Exception as e:
            print("Exception : CrawlClass.initialize()", e)