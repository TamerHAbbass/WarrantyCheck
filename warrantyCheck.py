from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time


class WarrantyCheck:
    
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r'c:\temp\firefoxdriver\geckodriver.exe')
        self.csv_list = []
        self.comp_dict = {}


    def scanCSV(self):
        with open('product.csv', 'r+') as f:
            csv_reader = csv.reader(f)
            _hostname = 0
            _serialNumber = 1
            _productNumber = 2
            for count, i in enumerate(csv_reader):
                self.comp_dict[count] = {
                        'hostname': i[_hostname],
                        'serialNumber': i[_serialNumber],
                    }
                if i[_productNumber]:
                    self.comp_dict[count]['productNumber'] = i[_productNumber]
                else:    
                    self.comp_dict[count]['productNumber'] = ''
                    

    def startFirefoxBrowser(self):
        self.driver.get("https://support.hp.com/us-en/checkwarranty/multipleproducts")


    def closeFirefoxBrowser(self):
        self.driver.close()


    def submitEntry(self):
        elem = self.driver.find_element_by_id('btnWFormSubmit')
        elem.send_keys(Keys.RETURN)
    
    def checkForProductNumber(self):
        package = []
        for i in range(15):
            try:
                elem = self.driver.find_element_by_id(f"wFormProductNum{i}")
                elem.send_keys(self.comp_dict[i]['productNumber'])
            except:
                pass
                
        print(package)
        return package

    
    
    def over20Submit(self):
        self.submitEntry()
        time.sleep(10)
        self.checkForProductNumber()
        self.submitEntry()
        time.sleep(10)
        elem = self.driver.find_elements_by_class_name('warrantyResultsTable')
        with open('warranty_info.txt', 'a+') as f:
            for i in elem:
                f.write(i.text + '\n')
        self.driver
        self.startFirefoxBrowser()
    
    
    def addSerialNumberToPage(self, num=None):
        index = 0
        
        for count, data in self.comp_dict.items():
                
            if index <= 15:
                elem = self.driver.find_element_by_id(f"wFormSerialNumber{index + 1}")
                print(count, data)
                print(data['serialNumber'])
                elem.send_keys(data['serialNumber'])
                index += 1
                
            if index == 15:
                self.over20Submit()
                index = 0
                
        self.over20Submit()
        index=0


if __name__ == '__main__':
    W = WarrantyCheck()
    W.scanCSV()
    W.startFirefoxBrowser()
    W.addSerialNumberToPage()