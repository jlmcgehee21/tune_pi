import helpers

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets, SelectField, SubmitField, IntegerField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    # create a list of value/description tuples
    ports = [(x, x) for x in helpers.list_all_serial_ports()]
    serial_ports = SelectField('Serial Port', choices=ports)

    obd_commands = [(x, x) for x in helpers.list_all_obd_commands()]
    obd = SelectMultipleField('OBD Pids', choices=obd_commands)

    pin_choices = [(x, x) for x in range(8)]
    pins = MultiCheckboxField('Analog Input Pins (External Sensors)', choices=pin_choices)

    time_options = [(10, '10 seconds'),
                    (30, '30 seconds'),
                    (60, '1 minute'),
                    (60*5, '5 minutes'),
                    (60*10, '10 minutes'),
                    (60*20, '20 minutes'),
                    (60*30, '30 minutes'),
                    (60*60, '1 hour')]

    seconds = SelectField('Logging Time', choices=time_options)

    submit = SubmitField('Start Logging')
