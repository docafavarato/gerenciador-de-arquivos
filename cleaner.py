import os
import sys
import shutil
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

if not os.path.exists(os.getcwd()+'\exported'):
    os.mkdir(os.getcwd()+'\exported')

root = os.getcwd()

class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None): # Configura a janela
        super(Ui, self).__init__(parent=parent)
        uic.loadUi('cleaner.ui', self)
        self.setWindowTitle('Gerenciador de arquivos')
        self.directoryinput.setText(os.getcwd())
        self.show()
        self.listar()
        
        # Conexão dos botões com os eventos
        self.list.itemSelectionChanged.connect(self.on_change) 
        self.filter.activated.connect(self.listar)
        self.erase.clicked.connect(self.remove)
        self.directorySelect.clicked.connect(self.get_directory)
        self.search.clicked.connect(self.get_directory_input)
        self.export_2.clicked.connect(self.export)
        
    def get_directory(self): # Retorna o caminho da pasta selecionada
        file = str(QFileDialog.getExistingDirectory(self, "Selecione uma pasta"))
        if not file:
            file = os.getcwd()
        else:   
            os.chdir(file)
            self.listar()
        
        self.directoryinput.setText(file)
        return file
    
    def get_directory_input(self):
        file = self.directoryinput.text()
        if file == '':
            pass
        else:
            try:
                os.chdir(file)
            except FileNotFoundError:
                pass
            self.listar()
        
    def listar(self): # Lista todos os arquivos que a pasta possue
        combo = self.filter.currentText()
        lista = self.list
        files = os.listdir()
        self.total.setText(f'Total de arquivos: {str(len(files))}')
        
        # Filtra os arquivos
        if combo == 'Todos':
                lista.clear()
                for file in files:
                    lista.addItem(file)
                   
        else:
            lista.clear()
            
            num = 0
            for file in files:
                if combo in file:
                    lista.addItem(file)
                    num += 1
                self.total.setText(f'Total de arquivos: {str(num)}') 
            else:
                lista.addItem(f"""Não existem arquivos ".{combo}" nesta pasta. """)
                 
            

    def on_change(self): # Retorna os arquivos selecionados e exibe a respectiva imagem
        if len([item.text() for item in self.list.selectedItems()]) > 1:
            pass
        else:
            for item in self.list.selectedItems():
                for a in [item.text()]:
                    self.picture.setPixmap(QtGui.QPixmap(a).scaled(400, 1000, QtCore.Qt.KeepAspectRatio))
        return [item.text() for item in self.list.selectedItems()]
        

    def remove(self): # Remove os arquivos selecionados
        items = Ui.on_change(self)
        for item in items:
            # Exibe uma janela de confirmação
            q = QMessageBox.question(self, 'PyQt5 message', f"Deseja remover {item}?", QMessageBox.Yes | QMessageBox.No)
            if q == QMessageBox.Yes:
                os.remove(item)
                self.list.clear()
                self.listar()
            else:
                pass
    
    def export(self): 
        items = Ui.on_change(self)
        for item in items:
            q = QMessageBox.question(self, 'PyQt5 message', f"Deseja exportar {item}?", QMessageBox.Yes | QMessageBox.No)
            
            if q == QMessageBox.Yes:
                shutil.copy(item, f'{root}\exported')
            else:
                pass
    

app = QApplication(sys.argv)
window = Ui()
app.exec_()
