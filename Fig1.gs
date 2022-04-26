lon1 = 30; lon2 = 300
lat1 = -30; lat2 = 30

'reinit'
'sdfopen domain.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'mask = mask'
'pac = pac'
'io = io'
'close 1'

'sdfopen UV.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'era11 = ave(Uobs,t=1,t=38)'
'era21 = ave(Vobs,t=1,t=38)'
'close 1'

'sdfopen DT.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'dteraim = ave(dtobs,t=1,t=38)'

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

'set map 1 1 5'
'set grid on 5 15 1'
'set grads off'

'set gxout shaded'
'set clevs -4.5 -4 -3.5 -3 -2.5 -2 -1.5 -1 -0.5 0.5 1 1.5 2 2.5 3 3.5 4 4.5'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'set xlopts 1 3 0.15'
'set ylopts 1 3 0.15'
'd dteraim'

'cbarn.gs 0.7 0 5.5 2.2 1'

nskip = '2'

'set arrscl 0.1 2.5'
'set arrlab off'
'set cthick 3'
'set ccolor 1'
'mag = sqrt(era11*era11+era21*era21)'
'd maskout(era11,mag-5);skip(era21,'nskip')'
rc = arrow(0.8,2.2,0.2,5,3,1)

'set xlopts 1 3 0.15'
'set ylopts 1 3 0.15'

'set gxout contour'
'set clab off'
'set ccolor 1'
'set cthick 4'
'set clevs 0.2 0.4 0.6 0.8'
'd mask'

'set strsiz 0.25'
'set string 1 c 6'
'draw string 5.5 5.9 Added heating domain'

'set strsiz 0.16'
'set string 1 l 5'
'draw string 8.8 2.07 K/day'
'draw string 1.1 2.07 m/s'

'set rgb 71 255 128 0'
'set rgb 81 0 0 255'

'set gxout contour'
'set clab off'
'set ccolor 81'
'set cthick 10'
'set clevs 0.6 0.999'
'd pac'
'set ccolor 71'
'set cthick 10'
'set clevs 0.6 0.999'
'd io'

'set strsiz 0.2'
'set string 81 bl 6'
'draw string 6.1 3 Pacific'
'set string 71 bl 6'
'draw string 1.675 3 Indian Ocean'

function arrow(x,y,len,scale,thick,col)
'set line 'col' 1 'thick
'draw line 'x-len/2.' 'y' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y+0.025' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y-0.025' 'x+len/2.' 'y
'set string 'col' c'
'set strsiz 0.15'
'draw string 'x' 'y-0.15' 'scale
return

