from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
import sys
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import dfa_driver as dfa
import dfa_viz_driver as dfav




class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.msgLabel = QLabel("")
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
        
 
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
    
class Window(QWidget):
    def __init__(self):
        
        super().__init__()
        width, height = 700, 850
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.initUI()

    def initUI(self):
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap("temp-dfa-graph2.png"))


    
class ImgLabel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImgLabel, self).__init__(parent)
        self.image = QPixmap("temp-dfa-graph.png")
         

class Main:
    NUMBER_OF_STATES = 5
    data = {'0': [1, 3, 5, 2, 4], '1': [2, 4, 1, 3, 5]}
    fig  = plt.figure()
    app = QApplication([])
    window = Window()
    table = None 
    Graph = None
    DFA = None
    
    photo = QPixmap("temp-dfa-graph2.png")
    finals = []
    def main(self, args):
        app = self.app
        window = self.window
        strings = ""
        def generate_graph_and_save(mat=[[1, 2], [3, 4], [5, 1], [2, 3], [4, 5]], finals=self.finals):
            fig = plt.figure()
            if self.Graph:
                self.Graph.clear()
            self.Graph = dfav.ret_plot(mat, fig, finals)
            fig.savefig('temp-dfa-graph2.png')
        
        def load():
            for i in range(self.NUMBER_OF_STATES):
                for j in range(2):
                    item = self.table.item(i,j)
                    self.data[f"{j}"][i] = int(item.text()) if item.text()!="" else 0
            

        def draw_table():
            table = TableView(self.data, self.NUMBER_OF_STATES, 2)
            table.setFixedSize(350, 230)
            layout1_2.addWidget(table)
            return table

        @pyqtSlot()
        def ok_button_driver():
            print(num_states.text())
            self.NUMBER_OF_STATES = int(num_states.text()) if num_states.text() != "" else 0
            self.table.deleteLater()
            self.data = {f'{i}':[0 for i in range(self.NUMBER_OF_STATES)] for i in range(2)}
            self.table = draw_table()

        @pyqtSlot()
        def press_refresh():

            self.finals = [int(i) for i in final_states.text().split(',')] if final_states.text() else []
            
            for i in range(self.NUMBER_OF_STATES):
                for j in range(2):
                    item = self.table.item(i,j)
                    self.data[f"{j}"][i] = int(item.text()) if item.text()!="" else 1
            
            mat = []
            for i in range(self.NUMBER_OF_STATES):
                mat.append([self.data['0'][i], self.data['1'][i]])
            
            generate_graph_and_save(mat, self.finals)
            
            
            mat += [self.finals]
            self.DFA = dfa.mat_builder(mat)
            
            update_image()

        @pyqtSlot()
        def press_generate():
            string_textbox.clear()
            if not self.DFA: 
                return
            self.string = ""
            dfa.set_rec(15)
            for string in dfa.accepted_strings_generator(self.DFA.states[0]):
                self.string += string + "\n"
            string_textbox.insertPlainText(self.string)
            dfa.set_rec(1000)


        @pyqtSlot()
        def cell_changed(table):
            try:
                table.cell = table.gui.table_widget.currentItem()
                table.triggered = table.cell.text()
                print("y", table.cell.text())
                print(table.triggered)
            except:
                pass
                
        def update_image():
            window.pic.setPixmap(QPixmap("temp-dfa-graph2.png"))

        
        button = QPushButton("Generate")
        

        button.clicked.connect(press_generate)

        layout1 = QHBoxLayout()
        # layout1.minimumSize(700, 400)
        # verticalSpacer = QSpacerItem(2, 2, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        layout1_1 = QVBoxLayout()
        # layout1_1.minimumSize(350, 400)

        label_generated_strings = QLabel("Generated Strings : ")
        layout1_1.addWidget(label_generated_strings)

        string_textbox = QPlainTextEdit()
        string_textbox.setFixedSize(330, 280)
        string_textbox.setReadOnly(True)

        layout1_1.addWidget(string_textbox)
        layout1_1.addWidget(button)
        
        

        layout1_2 = QVBoxLayout()
        
        
        layout1_2_1 = QFormLayout()
        l1 = QLabel("No. of States :")
        num_states = QLineEdit()

        layout1_2_1.addRow(l1, num_states)
        
        ok_button_no_states = QPushButton("OK")
        ok_button_no_states.clicked.connect(ok_button_driver)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(press_refresh)
        layout1_2_1.addRow(ok_button_no_states)
        
        
        layout1_2.addLayout(layout1_2_1)
        layout1_2.addWidget(refresh_button)
        label_enter_table = QLabel("Transition Table :")
        layout1_2.addWidget(label_enter_table)
        
        self.table = draw_table()
        
        #row for entering final states

        layout1_2_2 = QFormLayout()
        l2 = QLabel("Enter final States :")
        final_states = QLineEdit()

        layout1_2_2.addRow(l2, final_states)

        layout1_2.addLayout(layout1_2_2)

        layout1.addLayout(layout1_1)
        layout1.addLayout(layout1_2)



        window.setWindowTitle("2 alpha DFA")
        layout = QFormLayout()

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout1)

        update_image()
        
        # imlabel.setFixedSize(650, 750)
        
        layout_main.addWidget(window.pic)

        
        window.setLayout(layout_main)
        window.show()
        # table.show()
        sys.exit(app.exec_())
    
if __name__=="__main__":
    M = Main()
    M.main(sys.argv)