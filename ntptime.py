try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "192.168.11.1"

def ntptime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA + 28800
def localtime():
    tm=ntptime()
    days=int( tm / 86400 )
    seconds=tm % 86400
    tm_hour=int ( seconds / 3600 )
    tm_min= (int(seconds / 60)) % 60
    tm_sec= seconds % 60
    tm_wday= (days + 5) % 7
    if(tm_wday<0):
        tm_wday += 7
    DAYS_PER_400Y = (365*400 + 97)
    DAYS_PER_100Y = (365*100 + 24)
    DAYS_PER_4Y   = (365*4   + 1)
    qc_cycles = int(days / DAYS_PER_400Y)
    days %= DAYS_PER_400Y
    if (days < 0):
        days += DAYS_PER_400Y
        qc_cycles -=1
    c_cycles = int(days / DAYS_PER_100Y)
    if (c_cycles == 4):
        c_cycles -= 1
    days -= (c_cycles * DAYS_PER_100Y)
    q_cycles = int(days / DAYS_PER_4Y)
    if (q_cycles == 25):
        q_cycles -= 1
    days -= q_cycles * DAYS_PER_4Y
    years =int( days / 365)
    if (years == 4):
        years -= 1
    days -= (years * 365)
    tm_year=2000 + years + 4 * q_cycles + 100 * c_cycles + 400 * qc_cycles
    days_in_month = [31,29,31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month=0
    while days_in_month[month] <= days:
        days -= days_in_month[month]
        month += 1
    tm_mon  = month + 1
    tm_mday = days + 1
    days_since_jan1= [ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365 ]
    tm_yday= days_since_jan1[tm_mon-1]+tm_mday
    if( tm_mon >=3 and ( (tm_year % 4 ==0 and tm_year %100 !=0) or tm_year % 400 ==0 ) ):
        tm_mday +=1
    tm_localtime=(tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday)
    return tm_localtime


