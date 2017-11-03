'''
Ukrainian Hryvnia rate
The program that receives currency exchange data
from the National Bank of Ukraine (https://bank.gov.ua)
and CoinMarketCap (https://coinmarketcap.com)
From NBU:
tab1 -> current exchange rate for USD, EUR, PLN
tab2 -> currency rates on a certain date (now 60 currencies)
From CoinMarketCap:
tab3 -> top 10 cryptocurrencies (current list)

Requirements:
certifi==2017.7.27.1
chardet==3.0.4
idna==2.6
PyQt5==5.9
requests==2.18.4
sip==4.19.3
urllib3==1.22

'''
import sys
import requests
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QWidget, QAction, QTabWidget,
                             QLabel, QDesktopWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget,QTableWidgetItem,
                             QComboBox, QAction, QTextEdit,
                             QMessageBox)
from PyQt5.QtCore import QCoreApplication

api_nbu_current = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
api_nbu_date = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date='
# limit requests to no more than 10 per minute
api_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/?convert=UAH&limit=10'

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.center()
        self.setWindowTitle('Ukrainian Hryvnia rate') 
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        # add menu
        main_menu = self.menuBar() 
        file_menu = main_menu.addMenu('File')
        help_menu = main_menu.addMenu('Help')
        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)
        about_button = QAction('About', self)
        about_button.triggered.connect(self.about)
        help_menu.addAction(about_button)
        
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def about(self):
        QMessageBox.about(self, 'Ukrainian Hryvnia rate',
                          'Ukrainian Hryvnia rate\n'
                          'The program that receives currency exchange data\n'
                          'from the National Bank of Ukraine (https://bank.gov.ua)\n'
                          'and CoinMarketCap (https://coinmarketcap.com)\n'
                          '{}\n{}'.format('v1.0', '2017'))
 
class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(400,400) 
 
        # add tabs
        self.tabs.addTab(self.tab1,'Current NBU')
        self.tabs.addTab(self.tab2,'By date NBU')
        self.tabs.addTab(self.tab3,'Cryptocurrencies')

        # defining buttons for tabs
        self.current_button = QPushButton('Сurrent exchange rate', self)
        self.current_button.clicked.connect(self.make_request_current)
        self.date_button = QPushButton('Exchange rate for a certain date', self)
        self.date_button.clicked.connect(self.make_request_date)
        self.crypto_button = QPushButton('Cryptocurrencies CoinMarketCap', self)
        self.crypto_button.clicked.connect(self.make_request_crypto) 
        
        # create first tab
        self.usd_label = QLabel('United States dollar',self)
        self.usd_value = QLabel('UAH', self)
        self.eur_label = QLabel('Euro',self)
        self.eur_value = QLabel('UAH', self)
        self.pln_label = QLabel('Polish zloty',self)
        self.pln_value = QLabel('UAH',self)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.usd_label)
        hbox1.addWidget(self.usd_value)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.eur_label)
        hbox2.addWidget(self.eur_value)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.pln_label)
        hbox3.addWidget(self.pln_value)
        hbox_button = QHBoxLayout()
        hbox_button.addWidget(self.current_button)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addLayout(hbox1)
        self.tab1.layout.addLayout(hbox2)
        self.tab1.layout.addLayout(hbox3)
        self.tab1.layout.addLayout(hbox_button)
        self.tab1.setLayout(self.tab1.layout)

        # create second tab
        self.days = QComboBox(self)
        self.days_label = QLabel("days", self)
        self.create_combo_content(self.days, 1, 32)
        self.months = QComboBox(self)
        self.months_label = QLabel("months", self)
        self.create_combo_content(self.months, 1, 13)
        self.years = QComboBox(self)
        self.years_label = QLabel("years", self)
        self.create_combo_content(self.years, 2015, 2018)
        self.tip2 = QLabel('Precious metals: 1ozt = 31.1034768g',self)
        self.result_output = QTextEdit(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.days_label)
        hbox.addWidget(self.days)
        hbox.addWidget(self.months_label)
        hbox.addWidget(self.months)
        hbox.addWidget(self.years_label)
        hbox.addWidget(self.years)
        hbox_button = QHBoxLayout()
        hbox_button.addWidget(self.date_button)
        hbox_tip2 = QHBoxLayout()
        hbox_tip2.addWidget(self.tip2)
        hbox_result = QHBoxLayout()
        hbox_result.addWidget(self.result_output)
        
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addLayout(hbox)
        self.tab2.layout.addLayout(hbox_button)
        self.tab2.layout.addLayout(hbox_tip2)
        self.tab2.layout.addLayout(hbox_result)
        self.tab2.setLayout(self.tab2.layout)
        
        # create third tab
        self.tip3 = QLabel('Top 10 Cryptocurrencies',self)
        self.crypto = QTextEdit(self)
       
        hbox_tip3 = QHBoxLayout()
        hbox_tip3.addWidget(self.tip3)
        hbox_crypto = QHBoxLayout()
        hbox_crypto.addWidget(self.crypto)
        hbox_button = QHBoxLayout()
        hbox_button.addWidget(self.crypto_button)
        
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addLayout(hbox_tip3)
        self.tab3.layout.addLayout(hbox_crypto)
        self.tab3.layout.addLayout(hbox_button)
        self.tab3.setLayout(self.tab3.layout)
        
        # add tabs to widget        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def create_combo_content(self, label, start, stop):
        for el in range(start, stop):
            if el < 10:
                el = '0' + str(el)
            label.addItem('{}'.format(el))

    def make_request(self, api_url):
        try:
            res = requests.get(api_url)
            data=res.json()
            return data
        except:
            QMessageBox.information(self, 'Error', 'Sorry, the data is unavailable')
        
    def make_request_current(self):
        data = self.make_request(api_nbu_current)
        if data:
            result_list = [el for el in data if el['cc'] in ['USD', 'EUR', 'PLN']]
            self.usd_value.setText('{}:\n1{} = {:.2f} UAH'.format(result_list[0]['txt'],
                                                                 result_list[0]['cc'],float(result_list[0]['rate'])))
            self.eur_value.setText('{}:\n1{} = {:.2f} UAH'.format(result_list[1]['txt'],
                                                                 result_list[1]['cc'],float(result_list[1]['rate'])))
            self.pln_value.setText('{}:\n1{} = {:.2f} UAH'.format(result_list[2]['txt'],
                                                                 result_list[2]['cc'],float(result_list[2]['rate'])))
        
        
    def make_request_date(self):
        self.result_output.clear()
        days = self.days.currentText()
        months = self.months.currentText()
        years = self.years.currentText()
        data = self.make_request(api_nbu_date+years+months+days)
        if data:
            from operator import itemgetter
            data.sort(key=itemgetter('cc'))
            for el in data:
                self.result_output.append('1{} = {:.4f} UAH ({})'.format(el['cc'], float(el['rate']), el['txt']))

    def make_request_crypto(self):
        data = self.make_request(api_coinmarketcap)
        if data:
            for el in data:
                self.crypto.append('{}:\n1{} = {:.2f} UAH'.format(el['name'], el['symbol'], float(el['price_uah'])))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
