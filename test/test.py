import sys

sys.path.append("src")

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import *

from tentacle import Tentacle

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle_Test(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.draw()

        self.show()

    def draw(self):

        self.setWindowTitle("Tentacle Test")
        self.setFixedSize(1300, 800)
        self.setStyleSheet("background-color: #FFFFFF; border: 0px;")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)


        self.wdg_central  = QWidget()
        self.wdg_tentacle = Tentacle()

        self.ly_main = QVBoxLayout()
        self.ly_main.addWidget(self.wdg_tentacle)
        
        self.wdg_central.setLayout(self.ly_main)  

        self.setCentralWidget(self.wdg_central)

        self.activateWindow() 

        self.wdg_tentacle.render()

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""

if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = Tentacle_Test()   

    sys.exit(_app.exec_())



