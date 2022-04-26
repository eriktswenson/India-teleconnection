
meth = 'CPCCA'
sign = -1

panela = '0.5 7.5 4.3 10.8'
panelb = '0.5 7.5 1.5 4'

'reinit'
'sdfopen 'meth'.DT.io.nc'
'set lat -15 5'
'set lon 50 120'

'set display color white'; 'c'

** yellow -> red; light blue -> dark blue
'set rgb 21 255 250 170'; 'set rgb 41  200 255 255'
'set rgb 22 255 232 120'; 'set rgb 42  175 240 255'
'set rgb 23 255 192  60'; 'set rgb 43  130 210 255'
'set rgb 24 255 160   0'; 'set rgb 44   95 190 250'
'set rgb 25 255  96   0'; 'set rgb 45   75 180 240'
'set rgb 26 255  50   0'; 'set rgb 46   60 170 230'
'set rgb 27 225  20   0'; 'set rgb 47   40 150 210'
'set rgb 28 192   0   0'; 'set rgb 48   30 140 200'
'set rgb 29 165   0   0'; 'set rgb 49   20 130 190'

** combination
'set rgb 50   60 170 230'
'set rgb 51   95 190 250'
'set rgb 52  175 240 255'
'set rgb 53  255 250 170'
'set rgb 54  255 232 120'
'set rgb 55  255 192  60'
'set rgb 56  255 160   0'
'set rgb 57  255  96   0'
'set rgb 58  225  50   0'
'set rgb 59  165   0   0'


'set grads off'
'set grid off'
'set csmooth on'

'set parea 'panelb
'set gxout shaded'
'set xlopts 1 3 0.15'
'set ylopts 1 3 0.15'
'set xlabs 50E|60E|70E|80E|90E|100E|110E|120E'
'set ylabs 15S|10S|5S|EQ|5N'

'set clevs -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2'
'set ccols 46 45 44 43 42 41 0 21 22'
'd 'sign'*dt'
'set gxout contour'
'set ccolor 1'; 'set cthick 2'; 'set clab off'; 'set clopts -1 -1 0.2'
'set clevs -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2'
'd 'sign'*dt'
'cbarn.gs 0.6 1 7.8 2.7 0'
'set strsiz 0.18'
'draw string 7.6 4.3 K/day'
'close 1'

'sdfopen 'meth'.UV.ind.nc'
'set x 1 14'
'set y 1 11'
'set lat 7.5 35'
'set xlopts 1 3 0.15'
'set ylopts 1 3 0.15'
'u1 = uio1'; 'v1 = vio1'

'set parea 'panela
'mag = sqrt(u1*u1+v1*v1)'
'set gxout shaded'
'set clevs 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0'
'set ccols 0 51 52 53 54 55 56 57 58 59'
'set xlopts 1 3 0.15'
'set ylopts 1 3 0.15'
'set xlabs off'
'set ylabs |10N||15N||20N||25N||30N||35N'
'd mag'
'cbarn.gs 0.6 1 7.8 9 0'
'set strsiz 0.18'
'draw string 7.6 7.2 m/s'

'set gxout vector'
'set arrscl 0.05 0.075'
'set arrlab off'
'set cthick 8'
'set ccolor 1'
'd 'sign'*maskout(u1,mag-0.2);v1*'sign

'set strsiz 0.25'; 'set string 1 l 7'
'draw string 0.6 10.4 (a) EQUINOO mode'
'set string 1 l 7'
'draw string 0.6 3.6 (b)'

