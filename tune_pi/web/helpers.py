import obd
from serial.tools import list_ports

def list_all_obd_commands():
    commands = [obd.commands.__dict__.get(a).name
                for a in dir(obd.commands)
                if isinstance(obd.commands.__dict__.get(a), obd.OBDCommand)]

    return commands

def list_all_serial_ports():
    return [x.device for x in list_ports.comports()]

def form_to_sys_call(form):
    port = form.data['serial_ports']
    port = '/dev/ttys027'

    seconds = form.data['seconds']
    obd_pids = ','.join(form.data['obd'])

    analog_pins = ','.join(form.data['pins'])

    return 'bin/run {} {} {} {} tune_pi/web/static/logs/weblog.json'.format(port, obd_pids, analog_pins, seconds).split(' ')

