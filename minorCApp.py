import sys
import codecs
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from QCodeEditor import QCodeEditor
from MinorCSyntaxHighligther import MinorCSyntaxHighligther

from analyzer.ascParser import parse as ascParse, parser as ascParser
from analyzer.err import createReport
from interpreter.expression.struct import Struct
from interpreter.st import SymbolTable, Symbol
from interpreter.quadruple import Quadruple

import os

class Ui_augusApp(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__(None)
        self.setupUi()
        self.show()
        # reference to a file
        self.fileRef = ""
        self.fileSaved = True
        self.pantalla = None

    def setupUi(self):
        self.setObjectName("MinorC 0.1")
        self.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("augus.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        # -- ORGANIZADOR CENTRAL
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        # -- ORGANIZADOR INFERIOR
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        # -- TEXTO INDICANDO LA FILA ACTUAL EN EL TEXTO
        self.txtRow = QtWidgets.QLineEdit(self.centralwidget)
        self.txtRow.setEnabled(False)
        self.txtRow.setMinimumSize(QtCore.QSize(50, 0))
        self.txtRow.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtRow.setText("")
        self.txtRow.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtRow.setObjectName("txtRow")
        self.gridLayout_2.addWidget(self.txtRow, 0, 5, 1, 1)
        # -- ETIQUETA PARA LA COLUMNA DE TEXTO
        self.lblCol = QtWidgets.QLabel(self.centralwidget)
        self.lblCol.setTextFormat(QtCore.Qt.PlainText)
        self.lblCol.setWordWrap(False)
        self.lblCol.setObjectName("lblCol")
        self.gridLayout_2.addWidget(self.lblCol, 0, 2, 1, 1)
        # -- ETIQUETA PARA LA FILA DE TEXTO
        self.lblRow = QtWidgets.QLabel(self.centralwidget)
        self.lblRow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblRow.setTextFormat(QtCore.Qt.PlainText)
        self.lblRow.setObjectName("lblRow")
        self.gridLayout_2.addWidget(self.lblRow, 0, 4, 1, 1)
        # -- TEXTO INDICANDO LA COLUMNA ACTUAL EN EL TEXTO
        self.txtCol = QtWidgets.QLineEdit(self.centralwidget)
        self.txtCol.setEnabled(False)
        self.txtCol.setMinimumSize(QtCore.QSize(50, 0))
        self.txtCol.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtCol.setText("")
        self.txtCol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCol.setObjectName("txtCol")
        self.gridLayout_2.addWidget(self.txtCol, 0, 3, 1, 1)
        # -- ETIQUETA QUE INDICA EL ESTADO ACTUAL DE LA APLICACION
        self.lblStatus = QtWidgets.QLabel(self.centralwidget)
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout_2.addWidget(self.lblStatus, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        # -- SEPERADOR INPUT/OUTPUT
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        # -- ENTRADA DE CODIGO
        self.txtInput = QCodeEditor(self.splitter)
        font = QtGui.QFont("Courier New",12)
        self.txtInput.setFont(font)
        self.txtInput.setObjectName("txtInput")
        self.txtInput.textChanged.connect(self.txtInputChanged_action)
        self.txtInput.cursorPositionChanged.connect(self.txtInputCursorPositionChanged_action)

        self.test = MinorCSyntaxHighligther(self.txtInput.document())

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.splitter.setCollapsible(0, False)
        # -- BARRA DE MENÚ
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 962, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(self)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(self)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(self)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(self)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(self)
        self.actionPaste.setObjectName("actionPaste")
        self.actionFind = QtWidgets.QAction(self)
        self.actionFind.setObjectName("actionFind")
        self.actionReplace = QtWidgets.QAction(self)
        self.actionReplace.setObjectName("actionReplace")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAscendent_Without_Debugging = QtWidgets.QAction(self)
        self.actionAscendent_Without_Debugging.setObjectName("actionAscendent_Without_Debugging")
        self.actionGo_To = QtWidgets.QAction(self)
        self.actionGo_To.setObjectName("actionGo_To")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionGo_To)
        self.menuRun.addAction(self.actionAscendent_Without_Debugging)
        self.menuRun.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setWindowTitle("Augus 0.1 - fileName")
        self.lblCol.setText("Column")
        self.lblRow.setText("Row")
        self.lblStatus.setText("Ready")
        self.menuFile.setTitle("File")
        self.menuEdit.setTitle("Edit")
        self.menuRun.setTitle("Run")
        self.menuTools.setTitle("Tools")
        self.menuHelp.setTitle("Help")
        self.actionNew.setText("New")
        self.actionNew.setShortcut("Ctrl+N")
        self.actionOpen.setText("Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionSave.setText("Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave_As.setText("Save As")
        self.actionSave_As.setShortcut("Ctrl+Alt+S")
        self.actionExit.setText("Exit")
        self.actionUndo.setText("Undo")
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionRedo.setText("Redo")
        self.actionRedo.setShortcut("Ctrl+Y")
        self.actionCopy.setText("Copy")
        self.actionPaste.setText("Paste")
        self.actionCut.setText("Cut")
        self.actionCut.setText("Cut")
        self.actionCut.setShortcut("Ctrl+X")
        self.actionCopy.setText("Copy")
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionPaste.setText("Paste")
        self.actionPaste.setShortcut("Ctrl+V")
        self.actionFind.setText("Find")
        self.actionFind.setShortcut("Ctrl+F")
        self.actionReplace.setText("Replace")
        self.actionReplace.setShortcut("Ctrl+H")
        self.actionAbout.setText("About")
        self.actionAscendent_Without_Debugging.setText("Generate 3CA")
        self.actionAscendent_Without_Debugging.setShortcut("Ctrl+F5")
        self.actionGo_To.setText("Go To")
        self.actionGo_To.setShortcut("Ctrl+G")
        # -- File menu actions
        self.actionNew.triggered.connect(self.newFile_action)
        self.actionOpen.triggered.connect(self.openFile_action)
        self.actionSave.triggered.connect(self.saveFile_action)
        self.actionSave_As.triggered.connect(self.saveFileAs_action)
        self.actionExit.triggered.connect(self.close)
        # -- Edit menu actions
        self.actionGo_To.triggered.connect(self.goTo_action)
        # -- Run menu actions
        self.actionAscendent_Without_Debugging.triggered.connect(self.ascendentRun_action)
        # -- other actions
        self.actionReplace.setEnabled(False)
        self.actionAbout.triggered.connect(self.about_action)
    
    def newFile_action(self):
        """Checks reference of actual file being edited. If it's saved then just clear the input text, if it isn't saveFile is called"""
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
            elif msg == QtWidgets.QMessageBox.Cancel:
                return
            self.txtInput.setPlainText("")
            self.setWindowTitle('Augus 0.1 - untitled')
            self.lblStatus.setText("Not saved")
            self.fileRef = ""
        else:
            self.txtInput.setPlainText("")
            self.setWindowTitle('Augus 0.1 - untitled')
            self.lblStatus.setText("Not saved")
            self.fileRef = ""

    def saveFile_action(self):
        """Checks the existence of a reference to a file. If there is one, then the file is uploaded, else saveFileAs is called"""
        # there is a file reference?
        if not self.fileRef.strip():
            # there is not -> call savefileas
            self.saveFileAs_action()
        else:
            # there is -> upload file
            with codecs.open(self.fileRef, 'w', encoding='utf8') as f:
                f.write(self.txtInput.toPlainText())
            self.fileSaved = True
            self.lblStatus.setText('Saved')
    
    def saveFileAs_action(self):
        """Shows a file dialog to save a file at a directory. Retrieve file name and puts it as a reference to a file"""
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As', str(Path.home()))
        if fileName[0]:
            with codecs.open(fileName[0],'w', encoding='utf8') as f:
                f.write(self.txtInput.toPlainText())
            self.fileSaved = True
            self.lblStatus.setText('Saved')
            self.fileRef = fileName[0]
            self.setWindowTitle("Augus 0.1 - " + self.fileRef)

    def openFile_action(self):
        """Shows a file dialog to find a file. Retrieve file name and puts it as a reference to a file"""
        # call new file to verify if actual file is saved
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
            elif msg == QtWidgets.QMessageBox.Cancel:
                return
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open', str(Path.home()))
        if fileName[0]:
            try:
                with codecs.open(fileName[0],'r', encoding='utf8') as f:
                    self.txtInput.setPlainText(f.read())
                self.fileSaved = True
                self.lblStatus.setText('Saved')
                self.fileRef = fileName[0]
                self.setWindowTitle("Augus 0.1 - " + self.fileRef)
            except:
                QtWidgets.QMessageBox.critical(self,"Error", "Couldn't open file")

    def goTo_action(self):
        """Shows a input dialog. The user must enter a number or a coordinate, then the cursor is settled on that row number or coordinate"""
        txt, msg = QtWidgets.QInputDialog.getText(
            self, 'Go To',
            'Type the row number or a coordinate (row,col)'
        )
        if msg:
            txt = txt.strip()
            txt = txt.split(",")
            try:
                # remove ending and starting spaces
                tRow = int(txt[0].strip()) 
                # tRow cannot be less than 1
                tRow = tRow if tRow > 0 else 1
                # if txt array lenght is greater then 1 -> cast to int stripped txt[1] 
                tCol = int(txt[1].strip()) if len(txt) > 1 else 1
                # input user of tCol cannot be less than 1
                tCol = tCol if tCol > 0 else 1
                doc = self.txtInput.document()
                n = doc.blockCount()
                if tRow > n:
                    # tRow is greater than number of lines in txtInput
                    # replace tRow actual value to number of lines in txtInput
                    # get index for line number
                    tRow = n - 1
                else:
                    # get index for vertical movement
                    tRow -= 1
                self.txtInput.setFocus()
                # create and set cursor for line number tRow
                cursor = QtGui.QTextCursor(doc.findBlockByLineNumber(tRow))
                # gets Textblock
                crBlock = cursor.block()
                # gets text's length on textblock
                lenBlock = len(crBlock.text())
                # if text's length is less than tCol then the cursor is set at the end of the line
                tCol = (tCol-1) if tCol <= lenBlock else (lenBlock)
                # move cursor to tCol
                cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor,tCol)
                # set cursor to txtInput
                self.txtInput.setTextCursor(cursor)
            except:
                QtWidgets.QMessageBox.critical(
                    self, "Error",
                    "It's not possible to go to the indicated position"
                )

    def ascendentRun_action(self):
        txt = self.txtInput.toPlainText()
        t = ascParse(txt)
        print(t)
        try:
            Quadruple.QDict.clear()
            SymbolTable.St.clear()
            SymbolTable.IdxTempVar = 0
            Quadruple.IdxLabel = 0
            if t != None:
                t.firstRun()
                for k,v in SymbolTable.St.items():
                    print(f"{k}->(temp: {v.temp}, dimension: {v.dimension}, value: {v.value})")
                for q in Quadruple.QDict:
                    print(f"{q.r} <-> {q.arg1} {q.op} {q.arg2}")
            p = Quadruple.create3DCode()
            print(p)
            os.system(f"start {p}")
        except Exception as e:
            print("es gg ->", str(e))
        finally:
            try:
                SymbolTable.genRep()
                createReport()
            except:
                pass
        ascParser.restart()
        
    def txtInputCursorPositionChanged_action(self):
        txtcursor = self.txtInput.textCursor()
        txtRow = txtcursor.blockNumber()
        txtCol = txtcursor.positionInBlock()
        self.txtCol.setText(str(txtCol+1))
        self.txtRow.setText(str(txtRow+1))
        pass
        
    def txtInputChanged_action(self):
        self.fileSaved = False
        self.lblStatus.setText("Not Saved")

    def closeEvent(self, event):
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
                event.accept()
            elif msg == QtWidgets.QMessageBox.No:
                event.accept
            elif msg == QtWidgets.QMessageBox.Cancel:
                event.ignore()
    
    def about_action(self):
        QtWidgets.QMessageBox.information(
            self, "About",
            "Universidad de San Carlos de Guatemala\n" +
            "Facultad de Ingeniería\n"+
            "Escuela de Ciencias y Sistemas\n"+
            "Compiladores 2\n2do Semestre - 2020\n"+
            "────────────────────────\n"+
            "201602782\nSergio Fernando Otzoy Gonzalez",
            QtWidgets.QMessageBox.Ok
        )

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    u = Ui_augusApp()
    sys.exit(app.exec_())