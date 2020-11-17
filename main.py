import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
import Forms.main as mf  # Это наш конвертированный файл дизайна
import random
from my_classes.my_dialog import my_dialog 
import numpy as np
import os
import pickle
class ExampleApp(QtWidgets.QMainWindow, mf.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowIcon(QtGui.QIcon(self.tr("obj\ico.jpg")))
        self.pushButton.clicked.connect(self.add_element)  # Выполнить функцию browse_folder
                                                          # при нажатии кнопки
        self.pushButton_2.clicked.connect(self.remove_element)
        self.treeWidget.itemDoubleClicked.connect(self.call_dialog)     
        self.DATA_COLLECTIONS=[]
        self.count=0
        if  os.path.exists("obj\data.pkl"):
            with open('obj\data.pkl', 'rb') as f:
                self.DATA_COLLECTIONS= pickle.load(f)
            #print(self.DATA_COLLECTIONS)
            self.openGLWidget.update_data(self.DATA_COLLECTIONS)
            for i in self.DATA_COLLECTIONS:
                self.count=self.count+1
                curve=QtWidgets.QTreeWidgetItem(self.treeWidget)
                curve.setText(0,self.tr("curve_"+str(self.count)))
                curve.setText(1,self.tr(str(i["curve"])))
                points=QtWidgets.QTreeWidgetItem(curve)
                points.setText(0,self.tr("Width"))
                points.setText(1,self.tr(str(i["Width"])))
                points=QtWidgets.QTreeWidgetItem(curve)
                points.setText(0,self.tr("R"))
                points.setText(1,self.tr(str(i["R"])))
                points=QtWidgets.QTreeWidgetItem(curve)
                points.setText(0,self.tr("G"))
                points.setText(1,self.tr(str(i["G"])))
                points=QtWidgets.QTreeWidgetItem(curve)
                points.setText(0,self.tr("B"))
                points.setText(1,self.tr(str(i["B"])))
                for j in range(3):
                    points=QtWidgets.QTreeWidgetItem(curve)
                    points.setText(0,self.tr("Point: "+str(j)))
                    points.setText(1,self.tr(str(i["PointsX"][j])))
                    points.setText(2,self.tr(str(i["PointsY"][j])))
        
        #print( isinstance(self.treeWidget.parent(),QtWidgets.QWidget))
    
    def remove_element(self):
        item=self.treeWidget.selectedItems()
        if item and (item[0].parent() is None):
            self.DATA_COLLECTIONS.pop(self.treeWidget.indexOfTopLevelItem(item[0]))
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item[0])) 
            self.openGLWidget.update_data(self.DATA_COLLECTIONS)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Неверная операция")
            msg.setInformativeText("Необходимо выбрать корневой элемент")
            msg.setWindowTitle("Предупреждение")
            msg.exec_()
        

    def add_element(self):
        self.count=self.count+1
        curve=QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.DATA_COLLECTIONS.append(
            {
                "curve":3,
                "Width":random.randint(1,5),
                "R":random.randint(0,255),
                "G":random.randint(0,255),
                "B":random.randint(0,255),
                "PointsX":[random.randint(-20,20) for i in range(3)],
                "PointsY":[random.randint(-20,20) for i in range(3)]
            }
        )
        self.openGLWidget.update_data(self.DATA_COLLECTIONS)
        curve.setText(0,self.tr("curve_"+str(self.count)))
        curve.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["curve"])))
        points=QtWidgets.QTreeWidgetItem(curve)
        points.setText(0,self.tr("Width"))
        points.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["Width"])))
        points=QtWidgets.QTreeWidgetItem(curve)
        points.setText(0,self.tr("R"))
        points.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["R"])))
        points=QtWidgets.QTreeWidgetItem(curve)
        points.setText(0,self.tr("G"))
        points.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["G"])))
        points=QtWidgets.QTreeWidgetItem(curve)
        points.setText(0,self.tr("B"))
        points.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["B"])))
        
        
        for i in range(3):
            points=QtWidgets.QTreeWidgetItem(curve)
            points.setText(0,self.tr("Point: "+str(i)))
            points.setText(1,self.tr(str(self.DATA_COLLECTIONS[-1]["PointsX"][i])))
            points.setText(2,self.tr(str(self.DATA_COLLECTIONS[-1]["PointsY"][i])))

    def call_dialog(self,item):
        #print(item.parent())
        #if item.parent is None:
            #print(item.parent().indexOfChild(item))
        #else:
            #print(self.treeWidget.indexOfTopLevelItem(item))
        
        wnd=my_dialog(item)
        wnd.show()
        wnd.close_signal.connect(self.dialog_closed)
        wnd.exec_()

    def dialog_closed(self,item):
        index=0
        item1=None
        if item.parent() is None:
            index=self.treeWidget.indexOfTopLevelItem(item)
            item1=item
        else:
            index=self.treeWidget.indexOfTopLevelItem(item.parent())
            item1=item.parent()
        self.DATA_COLLECTIONS[index]["Width"]=int(item1.child(0).text(1))
        self.DATA_COLLECTIONS[index]["R"]=int(item1.child(1).text(1))
        self.DATA_COLLECTIONS[index]["G"]=int(item1.child(2).text(1))
        self.DATA_COLLECTIONS[index]["B"]=int(item1.child(3).text(1))
        x=0
        y=0
        tmpx=[]
        tmpy=[]
        for i in range(4,item1.childCount()):
            x=int(item1.child(i).text(1))
            y=int(item1.child(i).text(2))
            tmpx.append(x)
            tmpy.append(y)
        self.DATA_COLLECTIONS[index]["PointsX"]=tmpx
        self.DATA_COLLECTIONS[index]["PointsY"]=tmpy
        self.openGLWidget.update_data(self.DATA_COLLECTIONS)

    def closeEvent(self,event):
        with open('obj\data.pkl', 'wb') as f:
            pickle.dump(self.DATA_COLLECTIONS, f, pickle.HIGHEST_PROTOCOL)
        

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()