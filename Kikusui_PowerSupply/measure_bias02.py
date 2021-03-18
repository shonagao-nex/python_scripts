### ToF2 (Backward det.) bias readout

import visa
import time

rm = visa.ResourceManager()
inst = rm.open_resource('TCPIP::10.30.1.93::5025::SOCKET')

inst.read_termination  = '\n'
inst.write_termination = '\n'

#now = time.strftime('%Y/%m/%d %H:%M:%S')
#print(now)

voltage = inst.query('MEAS:VOLT?')
current = inst.query('MEAS:CURR?')

print('Voltage [V]: {0}'.format(voltage))
print('Current [A]: {0}'.format(current))

inst.close()
