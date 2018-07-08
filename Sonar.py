# Kevin Matheus Martins
# contato: kevinmmartins@gmail.com

# SISTEMA PARA MEDIDA DE NÍVEL DE UMA CAIXA DE ÁGUA

import serial
import time
from time import strftime

# Configura a serial
# para COM# o número que se coloca é n-1 no primeiro parâmetro. Ex COM9  valor 8
n_serial = raw_input("Digite o número da serial:")  # seta a serial
ser = serial.Serial("COM" + n_serial, 9600, timeout=0.5, parity=serial.PARITY_NONE)  # seta valores da serial

# Identificação da base e sensor

# ID_base = raw_input('ID_base:')
ID_base = 0
# ID_sensor = raw_input('ID_sensor:')
ID_sensor = 1

# Cria o vetor Pacote
Pacote = {}

while True:
    try:

        # Cria Pacote de 52 bytes com valor zero em todas as posições
        for i in range(1, 53):  # faz um array com 52 bytes
            Pacote[i - 1] = 0

        # Imprime na tela o menu de opções
        print('1 - Mede inclinacao:')
        print('s - Para sair:')

        Opcao = raw_input('Comando:')

        if Opcao == "1":  # troca id do sensor

            num_medidas = raw_input('Entre com o número de medidas = ')
            w = int(num_medidas)

            filename1 = strftime("sonar_%Y_%m_%d_%H-%M-%S.txt")
            print("Arquivo de log: %s" % filename1)
            S = open(filename1, 'w')

            for j in range(0, w):

                # Limpa o buffer da serial
                ser.flushInput()

                # Coloca no pacote o ID_sensor e ID_base
                Pacote[8] = int(ID_sensor)
                Pacote[10] = int(ID_base)

                # TX pacote - envia pacote para a base transmitir
                for i in range(1, 53):
                    TXbyte = chr(Pacote[i - 1])  # Deve converter para caracter em ASCII para escrever na serial
                    ser.write(TXbyte)

                # Tempo de espera para que receba a resposta do sensor
                time.sleep(0.1)

                # RX pacote - recebe o pacote enviado pelo sensor
                line = ser.read(52)  # faz a leitura de 52 bytes do buffer que recebe da serial pela COM

                # Checa se recebeu 52 bytes
                if len(line) == 52:

                    rssid1 = ord(line[0])
                    rssiu1 = ord(line[2])

                    if rssid1 > 128:
                        RSSId1 = ((rssid1 - 256) / 2.0) - 74

                    else:
                        RSSId1 = (rssid1 / 2.0) - 74

                    if rssiu1 > 128:
                        RSSIu1 = ((rssiu1 - 256) / 2.0) - 74

                    else:
                        RSSIu1 = (rssiu1 / 2.0) - 74

                    count = (Pacote[12])

                    # Leitura do AD0
                    ad0h = ord(line[17])  # inteiro
                    ad0l = ord(line[18])  # resto
                    AD0 = (ad0h * 256 + ad0l)

                    print(time.asctime(), j, 'Distância = ', AD0, 'cm', 'RSSId = ', RSSId1, ' RSSIu = ', RSSIu1)
                    print >> S, time.asctime(), j, 'Distância', ';', AD0, 'cm', '---', 'RSSId =', RSSId1, '---', 'RSSIu =', RSSIu1
                    time.sleep(0.5)
            S.close()
        else:
            ser.close()  # fecha a porta COM
            print('Fim da Execução')  # escreve na tela
            break

            ser.flushInput()
    except KeyboardInterrupt:
        ser.close()
        break
