# esp32-ntptime
Since there was no ntptime or machine.RTC module in the released micropython firmware of esp32, I reviewed the C code of timeutils.c (micropython-esp32/lib/timeutils/timeutils.c) and ported it to python. You can now get ntptime for esp32 with:
* import ntptime
* t=ntptime.localtime()
* print(t)
