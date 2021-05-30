import io
import time

import wiringpi

# One of the following MUST be called before using IO functions:

wiringpi.wiringPiSetupGpio()      # For sequential pin numbering
wiringpi.pinMode(21, wiringpi.OUTPUT)
wiringpi.digitalWrite(21, wiringpi.HIGH)
time.sleep(1)

wiringpi.pinMode(21, wiringpi.INPUT) # 恢复为INPUT模式, 0-8是上拉 其它是下拉

