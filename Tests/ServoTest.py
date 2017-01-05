# Test of writing servo position via Raspberry Pi GPIO pins
# Murray Ireland
# 22/12/2016

from BluetoothController import buttons

# Print buttons if active
if any(b > 0 for b in buttons.itervalues()):
    print buttons

