from PyQt5 import QtSql
from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox, 
	QTableView, QLabel, QPushButton, QLineEdit)

class Crud(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.name = QLabel('Название', self)
		self.nameEdit = QLineEdit(self)
		self.name.move(700, 10)
		self.nameEdit.setGeometry(700, 30, 250, 25)

		self.price = QLabel('Цена', self)
		self.priceEdit = QLineEdit(self)
		self.price.move(700, 70)
		self.priceEdit.setGeometry(700, 90, 250, 25)

		self.link = QLabel('Ссылка на страницу', self)
		self.linkEdit = QLineEdit(self)
		self.link.move(700, 130)
		self.linkEdit.setGeometry(700, 150, 250, 25)

		self.notation = QLabel('Примечание', self)
		self.notationEdit = QLineEdit(self)
		self.notation.move(700, 190)
		self.notationEdit.setGeometry(700, 210, 250, 25)

		self.btn_add = QPushButton('Создать', self)
		self.btn_add.move(700, 250)
		self.btn_update = QPushButton('Обновить', self)
		self.btn_update.move(785, 250)
		self.btn_delete = QPushButton('Удалить', self)
		self.btn_delete.move(870, 250)

		self.table = QTableView(self)

		self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
		self.db.setHostName('localhost')
		self.db.setDatabaseName('DBvishlist')
		self.db.setUserName('my_user')
		self.db.setPassword('password')

		self.model = QtSql.QSqlTableModel()
		self.model.setTable('vishlist')
		self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
		self.model.select()
		self.table.setModel(self.model)
		
		self.table.resize(685, 530)
		self.table.setColumnWidth(0, 33)
		self.table.setColumnWidth(1, 150)
		self.table.setColumnWidth(2, 100)
		self.table.setColumnWidth(3, 180)
		self.table.setColumnWidth(4, 180)

		self.setFixedSize(960, 550)
		self.setGeometry(300, 300, 960, 600)
		self.show()

		self.btn_add.clicked.connect(self.addToDb)
		self.btn_update.clicked.connect(self.updaterow)
		self.btn_delete.clicked.connect(self.delrow)

		self.i = self.model.rowCount()


	def addToDb(self):

		self.model.insertRows(self.i,1)
		self.model.setData(self.model.index(self.i,1),self.nameEdit.text())
		self.model.setData(self.model.index(self.i, 2), self.priceEdit.text())
		self.model.setData(self.model.index(self.i,3), self.linkEdit.text())
		self.model.setData(self.model.index(self.i,4), self.notationEdit.text())
		self.model.submitAll()
		self.i += 1


	def delrow(self):

		if self.table.currentIndex().row() > -1:
			self.model.removeRow(self.table.currentIndex().row())
			self.i -= 1
			self.model.select()
		else:
			QMessageBox.question(self,'Message', "Выберите строку для удаления", QMessageBox.Ok)
			self.show()


	def updaterow(self):

		if self.table.currentIndex().row() > -1:
			record = self.model.record(self.table.currentIndex().row())
			record.setValue("Название",self.nameEdit.text())
			record.setValue("Цена",self.priceEdit.text())
			record.setValue("Ссылка", self.linkEdit.text())
			record.setValue("Примечание", self.notationEdit.text())
			self.model.setRecord(self.table.currentIndex().row(), record)
		else:
			QMessageBox.question(self,'Message', "Выберите строку для обновления", QMessageBox.Ok)
			self.show()



if __name__ == '__main__':
	
	import sys
	app = QApplication(sys.argv)
	ex = Crud()
	sys.exit(app.exec_())

