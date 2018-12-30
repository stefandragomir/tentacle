
import math

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import *


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
"""

NODE -> EDGE -> NODE -> EDGE -> NODE

"""

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__draw()

    def __draw(self):

        self.scene = QGraphicsScene()
        self.view  = QGraphicsView(self.scene)

        self.ly_main = QHBoxLayout()
        self.ly_main.addWidget(self.view)

        self.setLayout(self.ly_main)


        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 400, 400)

        self.view.setCacheMode(QGraphicsView.CacheBackground)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.view.scale(0.8, 0.8)
        self.view.setMinimumSize(400, 400)

    def render(self):

        _nd1 = Tentacle_Node()
        _nd2 = Tentacle_Node()
        _nd3 = Tentacle_Node()

        _e1 = Tentacle_Node(_nd1, _nd2)
        _e2 = Tentacle_Node(_nd2, _nd3)

        self.scene.addItem(_nd1)
        self.scene.addItem(_nd2)
        self.scene.addItem(_nd3)


        self.scene.addItem(_e1)
        self.scene.addItem(_e2)

        _nd1.setPos(-50, -50)
        _nd2.setPos(0, -50)
        _nd3.setPos(50, -50)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle_Node(QGraphicsItem):

    def __init__(self,label="",icon=""):

        QGraphicsItem.__init__(self) 

        self.edges = []
        self.label = ""
        self.icon  = None

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)

    def boundingRect(self):

        _adjust = 2;
        
        _rect = QRectF( -10 - _adjust, -10 - _adjust, 23 + _adjust, 23 + _adjust)
        
        return _rect

    def paint(self,painter,option,wdg):

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)

        _gradient = QRadialGradient(-3, -3, 10)

        if option.state & QStyle.State_Sunken:

            _gradient.setCenter(3, 3)
            _gradient.setFocalPoint(3, 3)
            _gradient.setColorAt(1, QColor(Qt.yellow).light(120))
            _gradient.setColorAt(0, QColor(Qt.darkYellow).light(120))
        
        else:
            _gradient.setColorAt(0, Qt.yellow)
            _gradient.setColorAt(1, Qt.darkYellow)

        
        painter.setBrush(_gradient)
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def shape(self):

        _path = QPainterPath()
        
        _path.addEllipse(-10, -10, 20, 20)
    
        return _path

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle_Edge(QGraphicsItem):

    def __init__(self,source_node,dest_node,label=""):

        QGraphicsItem.__init__(self)

        self.label        = label 
        self.source_node  = source_node
        self.dest_node    = dest_node
        self.source_point =  QPointF()
        self.dest_point   =  QPointF()
        self.arrow_size   = 1

    def boundingRect(self):

        _pen_width = 1
        _extra     = (_pen_width + self.arrow_size) / 2.0

        _size = QSizeF(self.dest_point.x() - self.source_point.x(), self.dest_point.y() - self.dest_point.y())
        _rect = QRectF(self.source_point, _size).normalized().adjusted(-_extra, -_extra, _extra, _extra)

        return _rect

    def paint(self,painter,option,wdg):

        _line = QLineF(self.source_point, self.dest_point)

        if _line.length() > 0:

            painter.setPen( QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(_line)

            _angle = math.atan2(-_line.dy(), _line.dx())

            _source_arrow_p1 = self.source_point + QPointF(sin(_angle + M_PI / 3) * self.arrow_size,        cos(_angle + M_PI / 3) * self.arrow_size)
            _source_arrow_p2 = self.source_point + QPointF(sin(_angle + M_PI - M_PI / 3) * self.arrow_size, cos(_angle + M_PI - M_PI / 3) * self.arrow_size)
            _dest_arrow_p1   = self.dest_point   + QPointF(sin(_angle - M_PI / 3) * self.arrow_size,        cos(_angle - M_PI / 3) * self.arrow_size)
            _dest_arrow_p2   = self.dest_point   + QPointF(sin(_angle - M_PI + M_PI / 3) * self.arrow_size, cos(_angle - M_PI + M_PI / 3) * self.arrow_size)

            painter.setBrush(Qt.black);
            painter.drawPolygon( QPolygonF() << line.p1() << _source_arrow_p1 << _source_arrow_p2 )
            painter.drawPolygon( QPolygonF() << line.p2() << _dest_arrow_p1 << _dest_arrow_p2 )





