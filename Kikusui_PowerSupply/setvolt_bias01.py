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
  #  inst = rm.open_resource('TCPIP::172.25.26.82::5025::SOCKET')
    inst = rm.open_resource('TCPIP::10.30.1.98::5025::SOCKET')
     
    inst.read_termination  = '\n'
    inst.write_termination = '\r\n'

    val = readval()
    volt = float(val)

    inst.write('VOLT %.2lf' % volt)

    ReadVoltage = inst.query('MEAS:VOLT?')
    ReadCurrent = inst.query('MEAS:CURR?')

    print('===')
    print('Voltage [V]: {0}'.format(ReadVoltage))
    print('Current [A]: {0}'.format(ReadCurrent))
    print('===')

    inst.close()
