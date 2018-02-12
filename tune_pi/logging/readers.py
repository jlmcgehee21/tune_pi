import obd
try:
    import spidev
except:
    spidev = None

class OBDReader:
    def __init__(self, port, channels):
        self.conn = obd.OBD(port, conn_timeout=2)
        self.channels = channels


    def read(self, param):
        return param.desc, self.conn.query(param)

    def parser_callback(self, reading):
        value = reading[1].value
        val_tuple = value.to_tuple()
        return {'desc': reading[0], 'unit': val_tuple[1][0][0], 'value': val_tuple[0]}


class ADCReader:
    def __init__(self, channels):
        self.channels = channels
        self.v_ref = 3.3

        self.spi = self.__init_spi()

    def __init_spi(self):
        if spidev is not None:
            chip = 0
            spi = spidev.SpiDev()
            spi.open(0, chip)
            return spi
        return None

    def parser_callback(self, reading):
        channel = reading[0]
        data = reading[1]
        value = round((data * self.v_ref) / float(4096), 2)

        return {'desc': 'analog_channel_{}'.format(channel), 'unit': 'volts', 'value': value}

    def read(self, channel):
        if self.spi is not None:
            adc = self.spi.xfer2([6 + ((channel&4) >> 2),(channel&3) << 6, 0])
            data = ((adc[1] & 15) << 8) + adc[2]
            return channel, data
        return channel, 0


