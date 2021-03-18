import visa
import sys, time

def readval():
    try:
        val = float(sys.argv[1])
    except:
        sys.exit()
    return val

if __name__ == "__main__":
    rm = visa.ResourceManager()
    inst = rm.open_resource('TCPIP::10.30.1.93::5025::SOCKET')
#    inst = rm.open_resource('TCPIP::172.25.27.82::5025::SOCKET')
     
    inst.read_termination  = '\n'
    inst.write_termination = '\r\n'

    val = readval()
    volt = float(val)

    inst.write('VOLT %.1lf' % volt)

    inst.close()
