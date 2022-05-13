import serial
import serial.tools.list_ports 

# Brukervariabler som settes selv:
antallMaaling = 300

ports = serial.tools.list_ports.comports()
portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select Port: COM")

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portList[x])

emergency = []

trykk = []
tid_sek = []
tid_ms = []
magnet = []
tid = []
like_maalinger = []
godkjent_maaling = []

ser = serial.Serial(portVar,115200, timeout=0)


while len(trykk)<antallMaaling:
    if ser.in_waiting:
        datapakke = ser.readline().hex()
        print("datapakke før if = ", datapakke)

        if len(datapakke) < 14:
            databuf = datapakke
            emergency.append(databuf)
            datapatched = "".join(emergency)


            if len(datapatched) == 14:
                #print('reparert data: ' + datapatched)
                data = datapatched
                emergency.clear()

        else:
            data = datapakke
            trykk.append(int(data[0:2], 16))
            godkjent_maaling.append(int(data[2:4], 16))
            like_maalinger.append(int(data[4:6], 16))
            tid.append(int(data[10:14], 16) + (int(data[6:10], 16)/1000 ))
            magnet_mv = (int(data[14:18], 16)/4096)*3300
            #magnet.append(int(data[14:18], 16))
            magnet.append(magnet_mv)


# KODE FOR Å LOGGE BÅDE TRYKK OG MAGNET
file = open("Matlab_Data.txt", "w+", encoding='utf-8')
string =  "like_maalinger = "+ str(like_maalinger) + ";\n"+ "tid = "+ str(tid)+ "; \n" + "magnet = "+ str(magnet)+ ";\n" + "godkjent = " +str(godkjent_maaling)+ ";"
file.write(string)
file.close()