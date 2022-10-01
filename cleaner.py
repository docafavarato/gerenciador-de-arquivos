import os
import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox

class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None): # Configura a janela
        super(Ui, self).__init__(parent=parent)
        uic.loadUi('cleaner.ui', self)
        self.directoryinput.setText(os.getcwd())
        self.show()
        self.listar()
        
        # Conexão dos botões com os eventos
        self.list.itemSelectionChanged.connect(self.on_change) 
        self.filter.activated.connect(self.listar)
        self.erase.clicked.connect(self.remove)
        self.directorySelect.clicked.connect(self.get_directory)
        self.search.clicked.connect(self.get_directory_input)
        
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
            
            for file in files:
                if combo in file:
                    lista.addItem(file)     
            else:
                lista.addItem(f"""Não existem arquivos ".{combo}" nesta pasta. """)
                 
            

    def on_change(self): # Retorna os arquivos selecionados e exibe a respectiva imagem
        for item in self.list.selectedItems():
            for a in [item.text()]:
                self.picture.setPixmap(QtGui.QPixmap(a).scaled(400, 1000, QtCore.Qt.KeepAspectRatio))
                break
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
    

app = QApplication(sys.argv)
window = Ui()
app.exec_()