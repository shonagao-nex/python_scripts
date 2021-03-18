import sys, time, os, threading
import serial

class StageControl:
##### Initialize #####
    def __init__(self):
        self.isOpen = False
        self.event = threading.Event()

##### Convert #####
    def step2mm(self, pos):
        pos = float(pos) / 500
        return float(pos)

    def mm2step(self, pos):
        pos = float(pos) * 500
        return int(pos)

##### Wait Busy #####
    def WaitBusy(self):
        while True:
            time.sleep(0.5)
            val, status = self.Read()
            if(status == 'R'):
                break

##### Read Position #####
    def Read(self):
        data = (('Q:') + '\r\n').encode()
        self.ser.write(data)
        out = self.ser.readline()
        out = out.decode()
        out = out.strip()
        out = out.replace(' ','')
        out = out.split(',')
        return(int(out[0]), out[3]) #[0]:Position, [1]:CommandError, [2]:Limit, [3]:Busy-Ready

##### Set Original Position #####
    def Home(self):
        data = (('H:1') + '\r\n').encode()
        self.ser.write(data)
        out = self.ser.readline()
        out = out.decode()

##### Move Absolute Position #####
    def Move(self, pos):  # input pos = mm
        pos = self.mm2step(pos)
        if(pos<0 or pos>149900):
            return 'RangeOver'
        else:
            data = (('A:1+P%d' % pos) + '\r\n').encode()
            self.ser.write(data)
            out = self.ser.readline()
            out = out.decode()
            data = (('G:') + '\r\n').encode()
            self.ser.write(data)
            out = self.ser.readline()
            out = out.decode()
        return 'Moving'

##### Move Relative Position #####
    def MoveR(self, pos):  # input pos = mm
        pos = self.mm2step(pos)
        val, status = self.Read()
        pos = pos + val
        pos = self.step2mm(pos)
        status = self.Move(pos)
        return status

##### Stop Data #####
    def Stop(self):
        data = (('L:1') + '\r\n').encode()
        self.ser.write(data)
        out = self.ser.readline()
        out = out.decode()

##### Open Serial Port #####
    def Open(self, name):
        try:
#            self.ser = serial.Serial('/dev/ttyUSB1', 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.1)
            self.ser = serial.Serial(name, 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.1)
            self.isOpen = True
            self.ser.reset_input_buffer()
        except Exception as e:
            self.isOpen = False
            print(e);

        return self.isOpen

##### Close Serial Port #####
    def Close(self):
        self.Stop()
        if(self.isOpen):
            self.ser.close()
        self.isOpen = False

#if __name__ == "__main__":
#    try:
#        ser = StageControl()
#        ser.Open()
#        result = ser.Read()
#        print('Position: ', result[0])
##        ser.Home()
#        ser.Move(50000)
#        ser.WaitBusy()
#        ser.Move(0)
#        ser.WaitBusy()
#        ser.Close()
#    except KeyboardInterrupt:
#        ser.Stop()
#        result = ser.Read()
#        print('Position: ', result[0])
#        print('Stop!!')
