from ui_codes import Record
from utils import DealSql
from PyQt5.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QMessageBox


class RecordTab(Record.Ui_Form, QWidget):

    def __init__(self, callback, parent=None):
        super(RecordTab, self).__init__(parent)
        self.setupUi(self)
        self.sqlOp = DealSql.SqlOp('./data/data.db')
        self.sqlOp.connect()
        self.initUI()
        self.initClick()
        self.selectedRow = -1
        self.data = []
        self.callback = callback

    def initUI(self):
        self.tblSql.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblSql.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblSql.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblSql.verticalHeader().setVisible(False)

    def initClick(self):
        self.btnShowAll.clicked.connect(self.onBtnShowAll)
        self.btnLoadSql.clicked.connect(self.onBtnLoad)
        self.btnDelete.clicked.connect(self.onBtnDelete)
        self.tblSql.cellClicked.connect(self.clickOnOneLine)

    def onBtnShowAll(self):
        self.selectedRow = -1
        self.data = []
        self.tblSql.setRowCount(0)
        self.tblSql.clearContents()
        query = "SELECT * FROM base_info"
        queryResult = self.sqlOp.execQuery(query)
        self.tblSql.setRowCount(len(queryResult))
        for i in range(len(queryResult)):
            self.tblSql.setItem(i, 0, QTableWidgetItem(queryResult[i][0]))
            self.tblSql.setItem(i, 1, QTableWidgetItem(queryResult[i][1]))
            self.tblSql.setItem(i, 2, QTableWidgetItem(queryResult[i][2]))
            sex = "女" if queryResult[i][3] == 0 else "男"
            self.tblSql.setItem(i, 3, QTableWidgetItem(sex))
            self.data.append(queryResult[i])

    def onBtnLoad(self):
        if self.selectedRow == -1:
            QMessageBox.information(self, "提示", "未选中记录！", QMessageBox.Ok)
            return
        info = self.data[self.selectedRow]
        self.callback(info)

    def onBtnDelete(self):
        if self.selectedRow == -1:
            QMessageBox.information(self, "提示", "未选中记录！", QMessageBox.Ok)
            return
        info = self.data[self.selectedRow]
        delete = "DELETE FROM base_info WHERE record_time = '%s' AND birth_time = '%s'" % (info[0], info[1])
        self.sqlOp.execNonQuery(delete)
        self.tblSql.removeRow(self.selectedRow)
        self.selectedRow = -1

    def clickOnOneLine(self, row, column):
        self.selectedRow = row
