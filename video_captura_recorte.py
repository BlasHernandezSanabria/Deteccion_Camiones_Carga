# -*- coding: utf-8 -*-
import cv2
##############################################
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

def draw_line(video):
    global frame
    ret, frame = video.read()

    if ret:
        cv2.namedWindow('Marca la ROI de tu preferncia')
        cv2.setMouseCallback('Marca la ROI de tu preferncia', cortar_roi_imagen)
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

def aplicar_recorte_roi_video():
    ren_inicial, col_inicial = coordenadas[0][0], coordenadas[0][1]
    ren_final, col_final = coordenadas[1][0], coordenadas[1][1]
    print('X1: %d  Y1: %d   X2:%d   Y2:%d'%(ren_inicial, col_inicial, ren_final, col_final))
    print('coordenadas: ', coordenadas )
    return coordenadas



##############################################
#video = cv2.VideoCapture('avengers_era_ultron.avi')

if __name__ == '__main__':
    video = cv2.VideoCapture('C:\\Users\Andante\Documents\script_DB\'s\\temporales\codigos\python\PyDev\codigos_trailres\MOV04191.AVI')
    draw_line(video)

    while(video.isOpened()):
        ret, img = video.read()
        aplicar_recorte_roi_video()
        img = img[coordenadas[0][1]:coordenadas[1][1], coordenadas[0][0]: coordenadas[1][0]]
        print(img.shape)
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cv2.destroyAllWindows()
