from PyQt5 import QtWidgets, QtGui, QtCore
import Forms.dialog as df
import random
class my_dialog(QtWidgets.QDialog,df.Ui_Dialog):
    close_signal = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    def __init__(self,item):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(self.tr("obj\ico.jpg")))
        self.item=item
        self.item_parent=item.parent()
        self.lineEdit.setText(item.text(1))
        

        if item.text(0)=="R":
            self.label.setText(self.tr("Введите значение красного цвета:0-255"))
        if item.text(0)=="G":
            self.label.setText(self.tr("Введите значение зеленного цвета:0-255"))
        if item.text(0)=="B":
            self.label.setText(self.tr("Введите значение синего цвета:0-255"))
        if item.text(0)=="Width":
            self.label.setText(self.tr("Введите ширину линии"))
        if item.text(0)=="curve":
            self.label.setText(self.tr("Порядок кривой"))
        
        if item.text(2)  != self.tr(""):
            self.label.setText(self.tr("Координаты"))
            self.label_2.setText(self.tr("X"))
            self.label_3.setText(self.tr("Y"))
            self.lineEdit_2.setText(item.text(2))
        else:
            self.lineEdit_2.setParent(None)
            self.label_2.setParent(None)
            self.label_3.setParent(None)
        self.pushButton.clicked.connect(self.proceed)

    def proceed(self):
        if self.item_parent==None:
            self.proceed_root()
        else:
            self.proceed_item()
        self.close()
    def proceed_root(self):
        for i in range(4,self.item.childCount()):
            self.item.takeChild(4)
        for i in range (int(self.lineEdit.text())):
            point=QtWidgets.QTreeWidgetItem(self.item)
            point.setText(0,self.tr("Point: "+str(i)))
            point.setText(1,self.tr(str(random.randint(-10,10))))
            point.setText(2,self.tr(str(random.randint(-10,10))))

    def proceed_item(self):
        self.item.setText(1,self.lineEdit.text())
        self.item.setText(2,self.lineEdit_2.text())

    def closeEvent(self,event):
        self.close_signal.emit(self.item)
