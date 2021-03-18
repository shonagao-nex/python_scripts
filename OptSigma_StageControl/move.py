import StageControl
import sys

def readpos():
    try:
        name = sys.argv[1]
        pos  = float(sys.argv[2])
        print(name, pos)
    except:
        print('type python3 move.py position(mm)')
        sys.exit()
    return pos,name

if __name__ == "__main__":
    try:
        pos,name = readpos()
        ser = StageControl.StageControl()
        ser.Open(name)
        ser.Move(pos)
        ser.WaitBusy()
#        pos, status = ser.Read()
#        print('Position: ', pos)
        ser.Close()
    except KeyboardInterrupt:
        ser.Stop()
        print('Stop!!')
        pos, status = ser.Read()
        print('Position [mm]: ', pos)
        ser.Close()
