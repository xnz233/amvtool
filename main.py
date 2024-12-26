from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox
from PyQt5.QtCore import QThread
import sys
import os
import ffmpeg
from qt_material import apply_stylesheet

from Ui_main import Ui_MainWindow

filelist = []

class toAMV(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        c=1
        for file in filelist:
            stream = ffmpeg.input(file)
            dirStr, ext = os.path.splitext(file)
            filename = dirStr.split("\\")[-1]
            stream = ffmpeg.output(stream,f"{filename}.amv",ac=1,ar=22050,r=25,block_size=882,vstrict=-1)
            # stream = (
            # FFmpeg()
            # .option("y")
            # .input(file)
            # .output(
            #     f"{filename}.amv",
            #     ar=22050,
            #     ac=1,
            #     r=25,
            #     block_size=882,
            #     vstrict=-1
            #     )
            # )
            mainw.setWindowTitle(f"AMV转化器 转换中第{c}个视频中......")
            # @stream.on("progress")
            # def on_progress(progress: Progress):
            #     print(progress)
            ffmpeg.run(stream,overwrite_output=True)
            # stream.execute()
            c+=1
        mainw.setWindowTitle("AMV转化器 Made By 万能的小牛仔")
        QMessageBox.about(mainw,"AMV转化器","转换完毕！")
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
        self.ui.fileButton.clicked.connect(self.input_files)
        self.ui.clearButton.clicked.connect(self.clear_files)
        self.ui.startButton.clicked.connect(self.start)
        self.p = toAMV()
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # 当文件拖入此区域时为True
            event.accept()  # 接受拖入文件
        else:
            event.ignore()  # 忽略拖入文件

    def dropEvent(self, event):    # 本方法为父类方法，本方法中的event为鼠标放事件对象
        # 范围文件路径的Qt内部类型对象列表，由于支持多个文件同时拖入所以使用列表存放
        urls = [u for u in event.mimeData().urls()]
        for url in urls:
            file = url.path()[1:]
            self.ui.textBrowser.append(file)   # 将Qt内部类型转换为字符串类型
            filelist.append(file)

    def start(self):
        if filelist:
            self.p.start()
        else:
            QMessageBox.warning(mainw,"AMV转化器","文件列表为空！")
    def input_files(self):
        files, filetype = QFileDialog.getOpenFileNames()
        for file in files:
            self.ui.textBrowser.append(file)
            filelist.append(file)


    def clear_files(self):
        filelist = []
        mainw.ui.textBrowser.clear()

app = QApplication(sys.argv)
mainw = MainWindow()
apply_stylesheet(app, theme='dark_blue.xml')
mainw.show()
app.exec()
