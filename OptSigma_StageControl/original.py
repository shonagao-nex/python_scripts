import StageControl
import sys

if __name__ == "__main__":
    try:
        name = sys.argv[1]
        ser = StageControl.StageControl()
        ser.Open(name)
        ser.Home()
        ser.WaitBusy()
        pos, status = ser.Read()
        print('Position: ', pos)
        ser.Close()
    except KeyboardInterrupt:
        ser.Stop()
        print('Stop!!')
        result = ser.Read()
        print('Position: ', pos)
        ser.Close()
