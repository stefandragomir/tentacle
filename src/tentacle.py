
import math
import uuid

from PyQt5.QtCore     import *
from PyQt5.QtGui      import *
from PyQt5.QtWidgets  import *


"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle(QWidget):

    def __init__(self,node_width=100,node_height=100):

        QWidget.__init__(self)

        self.node_width  = node_width
        self.node_height = node_height
        self.nodes       = Tentacle_Nodes()

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

    def add(self,parent,node):

        node.nd_width  = self.node_width
        node.nd_height = self.node_height 

        if None == parent:
            self.nodes.add(node)            
        else:      
            parent.add(node)     

    def walk(self,node=None):

        _walked_nodes = []

        if None == node:
            for _node in self.nodes:
                _walked_nodes += _node.walk()
        else:
            _walked_nodes = node.walk()

        return _walked_nodes

    def count(self,node=None):

        _depth = 1

        if None == node:
            for _node in self.nodes:
                _depth += _node.depth()
        else:
            _depth = node.depth()

        return _depth

    def depth(self,node=None):

        _depth = []

        if None == node:
            for _node in self.nodes:
                _depth += _node.depth()
        else:
            _depth = node.depth()

        return max(_depth)

    def render(self):

        for _node in self.nodes:

            self.scene.addItem(_node)

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle_Node(QGraphicsItem):

    def __init__(self,label="",icon=None):

        QGraphicsItem.__init__(self) 

        self.id          = uuid.uuid4().hex
        self.label       = label
        self.icon        = None
        self.nd_width    = 100
        self.nd_height   = 100
        self.nd_x        = 0 
        self.nd_y        = 0
        self.is_visible  = True
        self.nodes       = Tentacle_Nodes()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)

    def boundingRect(self):
        
        _rect = QRectF(0, 0, self.nd_width, self.nd_height)
        
        return _rect

    def paint(self,painter,option,wdg):

        _pen = QPen(Qt.black, 0)

        painter.setPen(_pen)

        painter.drawRect(0, 0, self.nd_width, self.nd_height)

        painter.drawText(0, 0, self.label)

    def shape(self):

        _path = QPainterPath()
        
        _path.addRect(0, 0, self.nd_width, self.nd_height)
    
        return _path

    def add(self,node):

        self.nodes.add(node)

    def walk(self):

        _walked_nodes = [self]

        for _node in self.nodes:

            _walked_nodes += _node.walk()

        return _walked_nodes

    def count(self):

        _depth = 1

        for _node in self.nodes:

            _depth += _node.depth()

        return _depth

    def depth(self,start=0):

        _depth = [start + 1]

        for _node in self.nodes:

            _depth += _node.depth(start + 1)

        return _depth

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class Tentacle_Nodes(object):

    def __init__(self):

        self.objects = []

    def add(self,obj):

        self.objects.append(obj)  

    def __iter__(self):

        for obj in self.objects:

            yield obj

    def __getitem__(self,index):

        return self.objects[index]

    def __len__(self):

        return len(self.objects)

    def find_by_attribute(self,attribute,value):

        _object = None

        for _obj in self.objects:

            if getattr(_obj,attribute) == value:

                _object = _obj

        return _object

    def __contains__(self,obj):

        return obj.id in [_local_obj.id for _local_obj in self.objects]

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





