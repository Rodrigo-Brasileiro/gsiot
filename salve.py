import cv2
import cvzone
import time
import serial
from cvzone.PoseModule import PoseDetector
from cvzone.HandTrackingModule import HandDetector

# Porta serial do Arduino (ajuste conforme seu sistema)
arduino = serial.Serial('COM7', 9600)

# Vídeo de entrada (ou use 0 para webcam ao vivo)
video = cv2.VideoCapture("vd03.mp4") # Execute todos os vídeos para melhor compreensão da solução!

# Detectores
pose_detector = PoseDetector()
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)

# Sequência de gestos S.O.S
sequencia_sos = []
tempo_ultimo_gesto = 0
tempo_maximo_gesto = 4  # segundos para completar a sequência S-O-S

# FUNÇÃO DE CLAREAMENTO DE IMAGEM 
def clarear_imagem(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_clareado = clahe.apply(l)
    lab_clareado = cv2.merge((l_clareado, a, b))
    return cv2.cvtColor(lab_clareado, cv2.COLOR_LAB2BGR)

# LOOP PRINCIPAL
while True:
    check, img = video.read()
    if not check:
        break

    img = cv2.resize(img, (1280, 720))
    img = clarear_imagem(img)

    # DETECÇÃO DE POSE PARA QUEDA 
    pose_detector.findPose(img)
    pontos, bbox = pose_detector.findPosition(img, draw=False)

    if len(pontos) >= 27:
        x, y, w, h = bbox['bbox']
        cabeca = pontos[0][1]
        joelho = pontos[26][1]
        diferenca = joelho - cabeca

        if diferenca <= 0:
            cvzone.putTextRect(img, 'QUEDA DETECTADA', (x, y - 80), scale=3, thickness=3, colorR=(0, 0, 255))
            arduino.write(b'Q')  # Envia sinal de queda

    # DETECÇÃO DE GESTO S.O.S EM LIBRAS (S - O - S) 
    hands, img = hand_detector.findHands(img)

    if hands:
        for hand in hands:
            fingers = hand_detector.fingersUp(hand)

            # Etapa 1: punho fechado (S)
            if fingers == [0, 0, 0, 0, 0]:
                if len(sequencia_sos) == 0:
                    sequencia_sos.append('S')
                    tempo_ultimo_gesto = time.time()
                elif len(sequencia_sos) == 2 and sequencia_sos[-1] == 'O':
                    sequencia_sos.append('S')
                    tempo_ultimo_gesto = time.time()

            # Etapa 2: "O" (indicador e médio levantados)
            elif fingers == [0, 1, 1, 0, 0] and len(sequencia_sos) == 1 and sequencia_sos[0] == 'S':
                sequencia_sos.append('O')
                tempo_ultimo_gesto = time.time()

    # Mostrar progresso do gesto S.O.S
    texto_gesto = 'Gesto: ' + ''.join(sequencia_sos)
    cvzone.putTextRect(img, texto_gesto, (50, 650), scale=2, thickness=2, colorR=(255, 255, 0))

    # Validar se completou o S.O.S
    if sequencia_sos == ['S', 'O', 'S']:
        arduino.write(b'S')  # Envia sinal de S.O.S
        cvzone.putTextRect(img, 'SINAL DE SOCORRO!', (50, 100), scale=2, thickness=3, colorR=(255, 0, 0))
        sequencia_sos = []

    # Resetar sequência se tempo esgotar
    if time.time() - tempo_ultimo_gesto > tempo_maximo_gesto:
        sequencia_sos = []

    # Mostrar imagem final
    cv2.imshow('Monitoramento', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Encerramento
video.release()
cv2.destroyAllWindows()
