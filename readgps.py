import serial

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, write_timeout=1,xonxoff=False,rtscts=False,dsrdtr=False)

def sendUBXCommand(ser, payload):
    """Adds checksum to payload command and sends it to the serial port. Returns true if message received."""
    # First, lets create the checksum and add it to the end
    CK_A = CK_B = 0
    for b in payload[2:]:       # Ignore first sync bytes of command string
        CK_A += b
        CK_B += CK_A
    payload.append(CK_A & 0xff)
    payload.append(CK_B & 0xff)
    ser.reset_output_buffer()
    written = ser.write(payload)
    #print(str(written) + " bytes written\n")
    #AkorNak = ser.read(10)
    #print('{}'.format(AkorNak))
    #print(''.join('{:02x}'.format(a) for a in payload))

stationaryHeader = [0xB5, 0x62, 0x06, 0x24, 0x24, 0x00]
stationaryPayload = [0x00] * 36
stationaryPayload[1] = 0x40
stationaryPayload[22] = 100
stationaryPayload[28] = 100
stationaryCmd = stationaryHeader + stationaryPayload
payload = bytearray(stationaryCmd) # Convert to a bytearray
#sendUBXCommand(ser, payload)

mean_lat = 0
mean_lon = 0
mean_lat_old = 0
mean_lon_old = 0
count = 0
while 1:
    data = ser.readline()
    if '$GNGLL' in data:
        data = data.split(',')
        lat_deg = int(data[1][0:2])
        lat_min = float(data[1][2:])
        lon_deg = int(data[3][0:3])
        lon_min = float(data[3][3:])
        lat = lat_deg + lat_min/60.
        lon = lon_deg + lon_min/60.
        mean_lat_old = mean_lat
        mean_lon_old = mean_lon
        mean_lat = (mean_lat * count + lat) / (count + 1)
        mean_lon = (mean_lon * count + lon) / (count + 1)
        count += 1
#        print(str(mean_lat_old-mean_lat) + " " + str(mean_lon_old-mean_lon))
#        print(str(mean_lat) + " " + str(mean_lon))
        print(str(lat) + " " + str(lon))
