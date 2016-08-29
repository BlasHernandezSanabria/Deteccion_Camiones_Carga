#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Blas
#
# Created:     14/08/2016
# Copyright:   (c) Blas 2016
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
from PyQt4 import QtCore, QtGui, uic
import cv2

class DeteccionCamiones(QtGui.QMainWindow):
    def __init__(self):
        self.nom_archivo = ''
        self.ultima_ruta = 'C:\\Users'
        super(DeteccionCamiones, self).__init__()

        ##lectura del diseño UI
        uic.loadUi('C:\\Users\Andante\Documents\script_DB\'s\\temporales\codigos\python\gui\'s\conteo_vehiculos.ui', self)

        ##Establecer el estilo de los widgets
        self.barra_status.setStyleSheet(".QStatusBar{background-color:rgb(10, 10, 10); color : rgb(255,255,255); font-weight: bold}")
        self.boton_abrir.setStyleSheet(".QPushButton {background-color:rgb(200, 200, 200); padding: 2px 20px; text-align: center;\
                                                      border-radius: 4px; font-weight: bold}")
        self.boton_cortar.setStyleSheet(".QPushButton {background-color:rgb(200, 200, 200); padding: 2px 20px; text-align: center;\
                                                      border-radius: 4px; font-weight: bold}")
        self.boton_reset.setStyleSheet(".QPushButton {background-color:rgb(200, 200, 200); padding: 2px 20px; text-align: center;\
                                                      border-radius: 4px; font-weight: bold}")
        self.boton_iniciar.setStyleSheet(".QPushButton {background-color:rgb(200, 200, 200); padding: 2px 20px; text-align: center;\
                                                      border-radius: 4px; font-weight: bold}")
        
        ##conexión de los botones con sus metodos
        self.boton_abrir.clicked.connect(self.abrir_archivo)
        
        ##Establecer ShortCut's
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+o"), self, self.abrir_archivo)

        self.show()

    def abrir_archivo(self):
        print ('En abrir archivo')
        self.nom_archivo = QtGui.QFileDialog.getOpenFileName(self, 'Seleccionar archivo',self.ultima_ruta,
        "Video (*.avi *.AVI *.mov, *.MOV *.mp4 *.MP4)")
        if self.nom_archivo == '':
            self.barra_status.showMessage('Seleccione un archivo de video!!!',3000)
        else:
            print (self.nom_archivo)
            self.barra_status.showMessage('Abriendo archivo...' + self.nom_archivo.split('/')[-1], 1700)
            str_temp = self.nom_archivo.split('\\')
            print(str_temp)
            print('Abriendo archivo...' + str_temp[-1])
            self.ultima_ruta = self.nom_archivo.replace(str_temp[-1], '')
            self.nom_archivo = ''

    def set_label_img():
        video = cv2.VideoCapture(self.nom_archivo)
        ret, img_ = video.read()

        if ret:
            pixmap = QtGui.QPixmap(self.nom_archivo)
            self.label_img.setPixmap(pixmap)

def get_primos(num):
    primos = [1]
    for i in range(2,num):
      li = [j for j in range(2,i) if float(i)%j == 0 ]
      if len(li) == 0:
         primos.append(i)
    return primos

def k_prime_sum(num, k):
    lista_primos = get_primos(num)
    ##ToDo obtener todas las combinaciones de k elementos de la lista de primos


def main():
    app = QtGui.QApplication(sys.argv[1:])
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
     #Color del fondo de la ventana
    ventana = DeteccionCamiones()
    ventana.setPalette(palette)
    sys.exit(app.exec_())
    fgbg = cv2.createBackgroundSubtractorMOG()

if __name__ == '__main__':
    main()

