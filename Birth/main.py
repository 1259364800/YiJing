import sys
from win import YiJingWin
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = YiJingWin.YiJingWin()
    ui.show()
    sys.exit(app.exec_())
