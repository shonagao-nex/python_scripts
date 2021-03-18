#!/usr/bin/env python3
import StageControl
import sys

if __name__ == "__main__":
    try:
        name = sys.argv[1]
        ser = StageControl.StageControl()
        ser.Open(name)
        pos, status = ser.Read()
        pos = ser.step2mm(int(pos))
        print('%.3lf mm' % pos)
        ser.Close()
    except KeyboardInterrupt:
        ser.Stop()
        print('Stop!!')
        pos, status = ser.Read()
        pos = ser.step2mm(int(pos))
        print('%.3lf mm' % pos)
        ser.Close()
