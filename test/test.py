import sys

sys.path.append("src")

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import *

from tentacle import Tentacle
from tentacle import Tentacle_Node

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
        self.tentacle     = Tentacle()

        self.ly_main = QVBoxLayout()
        self.ly_main.addWidget(self.tentacle)
        
        self.wdg_central.setLayout(self.ly_main)  

        self.setCentralWidget(self.wdg_central)

        self.activateWindow() 

        self.draw_tentacles()

    def draw_tentacles(self):

        _node_1     = Tentacle_Node("Node 1",     None)
        _node_1_1   = Tentacle_Node("Node 1 1",   None)
        _node_1_2   = Tentacle_Node("Node 1 2",   None)
        _node_1_1_1 = Tentacle_Node("Node 1 1 1", None)
        _node_1_1_2 = Tentacle_Node("Node 1 1 2", None)
        _node_1_2_1 = Tentacle_Node("Node 1 2 1", None)
        _node_1_2_2 = Tentacle_Node("Node 1 2 2", None)

        self.tentacle.add(None,      _node_1)
        self.tentacle.add(_node_1,   _node_1_1)  
        self.tentacle.add(_node_1,   _node_1_2) 
        self.tentacle.add(_node_1_1, _node_1_1_1)
        self.tentacle.add(_node_1_1, _node_1_1_2)
        self.tentacle.add(_node_1_2, _node_1_2_1)
        self.tentacle.add(_node_1_2, _node_1_2_2)

        self.tentacle.render() 

        for _node in self.tentacle.walk():

            print(_node.label)  

        print(self.tentacle.depth())     

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
if __name__ == "__main__":

    _app = QApplication(sys.argv)  

    _ui  = Tentacle_Test()   

    sys.exit(_app.exec_())



