# -*- coding: utf-8 -*-
import sys,os
import subprocess
from PyQt4.QtGui import QMainWindow, QDesktopWidget, QSizePolicy, QWidget, QVBoxLayout, QAction, \
    QKeySequence, QLabel, QItemSelectionModel, QMessageBox, QFileDialog, QFrame, \
    QDockWidget, QProgressBar, QProgressDialog
from PyQt4.QtCore import QString, QStringList, SIGNAL, QSettings, QSize, QPoint, QVariant, QFileInfo, QTimer, pyqtSignal, QObject
import PyQt4.uic as uic

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupGui()
    ###
    ### GUI/Application setup
    ###___________________________________________________________________________________________
    def setupGui(self):
        self.ui = uic.loadUi(os.path.join('./gui/', "ftt.ui"), self)

        self.ui.cbb_weights.addItems(QStringList(['vgg16.ckpt',]))
        # self.ui.gv_image
        self.ui.le_img_index.setText('0')
        self.ui.le_img_number.setText('0')
        self.ui.le_faster_number.setText('0')
        # self.ui.cbb_weights.addItem(QString('vgg16.ckpt1'))
        # Show the UI.  It is important that this comes *after* the above
        # adding of custom widgets, especially the central widget.  Otherwise the
        # dock widgets would be far to large.
        self.center()
        self.ui.show()

        ## connect action signals
        self.connectActions()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def connectActions(self):
        self.ui.btn_start.clicked.connect(self.slots_btn_start_train)
        self.ui.btn_reset.clicked.connect(self.slots_btn_reset_train)
        # detect page
        self.ui.btn_add_detect_model.clicked.connect(self.slots_btn_add_detect_model)
        self.ui.btn_detect_read_path.clicked.connect(self.slots_btn_detect_read_path)
        self.ui.btn_detect_save_path.clicked.connect(self.slots_btn_detect_save_path)
        self.ui.btn_detect_save_img_path.clicked.connect(self.slots_btn_detect_save_img_path)
        self.ui.btn_start_detect.clicked.connect(self.slots_btn_start_detect)
        self.ui.btn_open_json_file.clicked.connect(self.slots_btn_open_json_file)


        pass

    # slots

    def slots_btn_start_train(self):
        # print(self.ui.cbb_weights.currentText())
        p = subprocess.Popen('ps aux', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # self.ui.plainTextEdit.setPlainText(self.ui.cbb_weights.currentText())
        self.ui.textEdit.setText(self.ui.cbb_weights.currentText())

        # p.stdout.readlines()
        for line in p.stdout.readlines():
            self.ui.textEdit.append(QString(line))
        self.ui.progressBar.setValue(100)

    def slots_btn_reset_train(self):
        self.ui.textEdit.clear()
        self.ui.progressBar.setValue(0)

    #
    def slots_btn_start_detect(self):
        model = str(self.ui.cbb_detect_model.currentText())
        data_path = str(self.ui.le_detect_read_path.text())
        save_json_path = str(self.ui.le_detect_save_path.text())
        save_imgs_path = str(self.ui.le_detect_save_img_path.text())
        print('model', model, '\ndata_path', data_path,\
            '\nsave_json_path', save_json_path, '\nsave_imgs_path', save_imgs_path)
        os.system('cd /home/wanghao/tf-faster-rcnn \n pwd')
        os.system('pwd')
        pass
    def slots_btn_add_detect_model(self):
        fileName = QFileDialog.getOpenFileName(self, u'add detect model',
                                               u'.', u'DL model(*.ckpt.index);;')
        print(fileName)
        # self.ui.cbb_detect_model.addItem(QString('vgg16.ckpt'))
        self.ui.cbb_detect_model.addItem(fileName)
    def slots_btn_detect_read_path(self):
        read_path = QFileDialog.getExistingDirectory(self)
        self.ui.le_detect_read_path.setText(read_path)

    def slots_btn_detect_save_img_path(self):
        save_img_path = QFileDialog.getExistingDirectory(self)
        self.ui.le_detect_save_img_path.setText(save_img_path)

    def slots_btn_detect_save_path(self):
        save_path = QFileDialog.getSaveFileName(self, 'save file', \
                    "faster.json" , "json files (*.json);;all files(*.*)")
        self.ui.le_detect_save_path.setText(save_path)

    def slots_btn_open_json_file(self):
        path = self.ui.le_detect_save_path.text()

        if os.path.exists(path):
            os.system('nautilus ' + str(path))
        else:
            QMessageBox.information(self, 'tips', 'file not found!')