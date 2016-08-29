# -*- coding: utf-8 -*-
import numpy as np
import cv2
import copy
#import video_captura_recorte as recorte
##################################################################################

class DeteccionCamiones():
    
    def __init__(self):
        self.area_contorno = 0
        self.area_mascara_eliminar = 0
        self.area_minima_conteo = 0
        self.renglon_linea_conteo = 0

        coordenadas = []
        coordenadas_linea = []
        cortando = False
        modo = False

    def cortar_roi_imagen(event, x, y, flags, param):
        global coordenadas, coordenadas_linea, cortando, modo

        if modo == False:
            if event == cv2.EVENT_LBUTTONDOWN:
                print ('cortando')
                coordenadas = [(x,y)]
            elif event == cv2.EVENT_LBUTTONUP:
                cortando = True
                print ('Se cortó')
                coordenadas.append((x, y))
                print ('Dibujando')
                print(coordenadas)
                cv2.rectangle(frame,coordenadas[0], coordenadas[1], (0,50,255), 2)
                cv2.imshow('Marca la ROI de tu preferncia', frame)

        elif modo == True:
            if event == cv2.EVENT_LBUTTONDOWN:
                print ('inicio (%d,%d)'%(x,y))
                coordenadas_linea = [(x,y)]
            elif event == cv2.EVENT_LBUTTONUP:
                modo = False
                print ('fin (%d,%d)'%(x,y))
                coordenadas_linea.append((x,y))
                print('Dibujando')
                cv2.line(frame, coordenadas_linea[0], coordenadas_linea[1], (255,100,50), 2)
                #cv2.imshow('Linea y rectangulo',frame)

    def eliminar_areas(imagen, area):
        imagenCopia = copy.copy(imagen)
        imagen_and = np.ones(imagen.shape, dtype='uint8')
        mascara = np.ones(imagen.shape, dtype='uint8')
        contornos_finales = []
        im2, contours, hierachy = cv2.findContours(imagen, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        for contorno in contours:
            if cv2.contourArea(contorno) > area:
                cv2.drawContours(mascara, [contorno], 0, (255,255,0), 2)
                contornos_finales.append(contorno)
            imagen_and = imagenCopia * mascara
        return (mascara, contornos_finales)

    def dibujar_contornos(frame, contornos, camiones, renglon):

        for contorno in contornos:
                ###1) Valor a configurar->self.area_contorno = 0
                if cv2.contourArea(contorno) > 680:
                    (x,y,w,h) = cv2.boundingRect(contorno)
                    x2 = x+w
                    y2 = y+h

                    rect = cv2.minAreaRect(contorno)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
    
                    m = cv2.moments(contorno)
                    centroX = int(m['m10']/m['m00'])
                    centroY = int(m['m01']/m['m00'])

                    #print('X1:%d Y1:%d | X2:%d Y2:%d'%(x, y, x+w, y+h))
                    #print('Cx: ', centroX, 'Cy: ', centroY)
                    area = (y2-y) * (x2-x)

                    centriodeX = int(x+((x2-x)/2))
                    centriodeY = int(y+((y2-y)/2))
                    #print('Area: %f'%area )
                    #print('CentroX:', centriodeX, 'CentroY:', centriodeY)
                    print('renglon: ',renglon, 'centroideY:', centriodeY)
                    print('Area cv2:', cv2.contourArea(contorno))
                    print('Area rectangulo:', area)

                    ###2) Valor a configurar -->self.area_minima_conteo = 0
                    if area > 2300 and renglon == centriodeY:
                        #cv2.rectangle(frame,(x,y),(x2,y2),(0,110,253),2)
                        cv2.drawContours(frame,[contorno], 0, (0,110,253),2)
                        cv2.drawContours(frame, [box], 0, (255,255,255),3)
                        camiones+=1
                        #print('Camiones: ', camiones)
                        print('Presiona una tacla para contunuar: ', camiones)

                        cv2.waitKey(0)
                    else:
                        #cv2.rectangle(frame,(x,y),(x2,y2),(0,255,0),2)
                        cv2.drawContours(frame, [contorno], 0, (0,255,0),2)
                        cv2.drawContours(frame, [box], 0, (255,255,255,1))

                    #Primer punto (click izquierdo del mouse)
                    cv2.circle(frame,(x,y), 2, (255,0,0), -1)
                    #Segundo punto (donde suelta el boton del mouse)
                    cv2.circle(frame,(x2,y2), 2, (0,0,255), -1)
                    #Centroide
                    cv2.circle(frame,(centriodeX, centriodeY), 2, (3,96,255), -1)
                    #ToDo calcular el area del los rectangulos y descartar los carros
        return (frame, camiones)
    
    def aplicar_recorte_roi_video():
        ren_inicial, col_inicial = coordenadas[0][0], coordenadas[0][1]
        ren_final, col_final = coordenadas[1][0], coordenadas[1][1]
        print('X1: %d  Y1: %d   X2:%d   Y2:%d'%(ren_inicial, col_inicial, ren_final, col_final))
        print('coordenadas: ', coordenadas )
        return coordenadas
    
    def draw_line(video):
        global frame
        ret, frame = video.read()
    
        if ret:
            cv2.namedWindow('Marca la ROI de tu preferncia')
            cv2.setMouseCallback('Marca la ROI de tu preferncia', self.cortar_roi_imagen)
            img_copia = frame.copy()
            
            while(1):
                
                cv2.imshow('Marca la ROI de tu preferncia', frame)
                tecla = cv2.waitKey(1) & 0xFF
    
                if tecla == ord('r'):
                    print('reset area y linea')
                    cortando = False
                    frame = img_copia.copy()
                    coordenadas = []
                elif tecla == ord('l'):
                    print('modo linea')
                    modo = True
                elif tecla == ord('c'):
                    print('continuar')
                    break

        cv2.destroyAllWindows()

##################################################################################
#cap = cv2.VideoCapture("/home/laboratorio/Escritorio/id_trailers/chrisss/videos/MOV04172.AVI")
if __name__ == '__main__':
    det_camiones = DeteccionCamiones()
    camiones = 0
    cap = cv2.VideoCapture('C:\\Users\Andante\Documents\script_DB\'s\\temporales\codigos\python\PyDev\codigos_trailres\MOV04191.AVI')
    ###LINE_3_45  = np.array([[0, 0, 1], [0, 1, 0], [0, 0, 1]], dtype=np.uint8)
    mascara_fondo = cv2.createBackgroundSubtractorMOG2(history= 300, varThreshold = 64, detectShadows=False)
    print ('Acá 2')
    ret, referencia_corte = cap.read()
    print ('Acá 3')
    det_camiones.draw_line(cap)
    print ('Acá 4')
    coordenadas = det_camiones.aplicar_recorte_roi_video()
    print ('Acá 5')
    referencia_corte = referencia_corte[coordenadas[0][1]:coordenadas[1][1], coordenadas[0][0]: coordenadas[1][0]]
    mascara_relleno = np.zeros((referencia_corte.shape[0]+2, referencia_corte.shape[1]+2), dtype=np.uint8)

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = frame[coordenadas[0][1]:coordenadas[1][1], coordenadas[0][0]: coordenadas[1][0]]
        macara_primerPlano = mascara_fondo.apply(frame)
        ###cv2.imshow('Fgmask', macara_primerPlano)
        cv2.floodFill(macara_primerPlano, mascara_relleno, (0, 0), 255)
        ###cv2.imshow('Flooding', macara_primerPlano)
        
        ###3) Valor a configurar -->self.area_mascara_eliminar = 0
        (macara_primerPlano,contornos) = det_camiones.eliminar_areas(macara_primerPlano, 400)
        ##print(contornos)
        cv2.imshow('Eliminar areas', macara_primerPlano)

        #No ayuda
        #dilated_filter_1 = cv2.dilate(macara_primerPlano, LINE_3_45)
        
        ###4) Valor a configurar -->self.renglon_linea_conteo
        renglon_linea = frame.shape[0] - int(frame.shape[0]*0.33)
        frame, camiones = det_camiones.dibujar_contornos(frame,contornos, camiones, renglon_linea)
        cv2.line(frame, (1,renglon_linea), (frame.shape[1],renglon_linea), (255,0,0),2)

        #cv2.imshow('frame',dilated_filter_1)
        cv2.imshow('Detección', frame)
        k = cv2.waitKey(30) & 0xff

        if k == 27:
            print('P1: ', coordenadas[0][1], ',' ,coordenadas[1][1])
            print('P2: ', coordenadas[0][0], ',' ,coordenadas[1][0])
            print(frame.shape)
            break

    print('Camiones totales: ', camiones)
    cap.release()
    cv2.destroyAllWindows()
    