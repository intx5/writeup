import math, sys, datetime

def jd(dt):
    y, m = (dt.year, dt.month)
    d = dt.day + (dt.hour + (dt.minute + (dt.second + dt.microsecond / 1000000.0) / 60) / 60) / 24
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5

def solar(dt, lat, lon):
    J = jd(dt)
    T = (J - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360
    M = 357.52911 + T * (35999.05029 - 0.0001537 * T)
    e = 0.016708634 - T * (4.2037e-05 + 1.267e-07 * T)
    C = math.sin(math.radians(M)) * (1.914602 - T * (0.004817 + 1.4e-05 * T)) + math.sin(math.radians(2 * M)) * (0.019993 - 0.000101 * T) + math.sin(math.radians(3 * M)) * 0.000289
    true_long = L0 + C
    omega = 125.04 - 1934.136 * T
    app_long = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    e0 = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60
    eps = e0 + 0.00256 * math.cos(math.radians(omega))
    decl = math.degrees(math.asin(math.sin(math.radians(eps)) * math.sin(math.radians(app_long))))
    y = math.tan(math.radians(eps / 2)) ** 2
    EoT = 4 * math.degrees(y * math.sin(2 * math.radians(L0)) - 2 * e * math.sin(math.radians(M)) + 4 * e * y * math.sin(math.radians(M)) * math.cos(2 * math.radians(L0)) - 0.5 * y * y * math.sin(4 * math.radians(L0)) - 1.25 * e * e * math.sin(2 * math.radians(M)))
    utc_min = dt.hour * 60 + dt.minute + dt.second / 60 + dt.microsecond / 60000000.0
    tst = (utc_min + EoT + 4 * lon) % 1440
    H = tst / 4 - 180
    phi = math.radians(lat)
    dec = math.radians(decl)
    hr = math.radians(H)
    cosz = math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(hr)
    cosz = max(-1, min(1, cosz))
    z = math.acos(cosz)
    elev = 90 - math.degrees(z)
    sinA = -math.cos(dec) * math.sin(hr) / math.sin(z) if math.sin(z) != 0 else 0
    cosA = (math.sin(dec) - math.sin(phi) * cosz) / (math.cos(phi) * math.sin(z)) if math.cos(phi) * math.sin(z) != 0 else 1
    A = math.degrees(math.atan2(sinA, cosA)) % 360
    return (elev, A, decl, EoT, tst / 60)
if __name__ == '__main__':
    dt = datetime.datetime(2026, 6, 27, 18, 10, 0)
    cities = [('London', 51.5074, -0.1278), ('Paris', 48.8566, 2.3522), ('Brussels', 50.8503, 4.3517), ('Amsterdam', 52.3676, 4.9041), ('Cologne', 50.9375, 6.9603), ('Frankfurt', 50.1109, 8.6821), ('Munich', 48.1351, 11.582), ('Zurich', 47.3769, 8.5417), ('Milan', 45.4642, 9.19), ('Berlin', 52.52, 13.405), ('Vienna', 48.2082, 16.3738), ('Lyon', 45.764, 4.8357), ('Bordeaux', 44.8378, -0.5792), ('Nantes', 47.2184, -1.5536), ('Lille', 50.6292, 3.0573), ('Dublin', 53.3498, -6.2603), ('Manchester', 53.4808, -2.2426), ('Hamburg', 53.5511, 9.9937), ('Copenhagen', 55.6761, 12.5683), ('Stuttgart', 48.7758, 9.1829), ('Geneva', 46.2044, 6.1432), ('Turin', 45.0703, 7.6869), ('Bologna', 44.4949, 11.3426), ('Prague', 50.0755, 14.4378)]
    print('time', dt, 'UTC')
    for n, la, lo in cities:
        e, A, d, eot, tst = solar(dt, la, lo)
        print(f'{n:12s} lat={la:6.2f} lon={lo:7.2f} elev={e:6.2f} az={A:7.2f} decl={d:6.3f} tst={tst:5.2f}')
