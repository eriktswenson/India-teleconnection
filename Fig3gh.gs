
panela = '0.5 5.3 6.15 8.15'; panelb = '5.7 10.5 6.15 8.15'
lon1 = 80; lon2 = 110; lon3 = 150; lon4 = 200

'reinit'
'sdfopen DT.nc'
'set t 1 38'
'set x 1'; 'set y 1'
'dterai1 = aave(dtobs,lon='lon1',lon='lon2',lat=-10,lat=10)'
'dterai2 = aave(dtobs,lon='lon3',lon='lon4',lat=-10,lat=10)'
'dtctl1 = aave(dtctl,lon='lon1',lon='lon2',lat=-10,lat=10)'
'dtctl2 = aave(dtctl,lon='lon3',lon='lon4',lat=-10,lat=10)'
'dthtg1 = aave(dthtg,lon='lon1',lon='lon2',lat=-10,lat=10)'
'dthtg2 = aave(dthtg,lon='lon3',lon='lon4',lat=-10,lat=10)'
'dtadd1 = aave(dtadd,lon='lon1',lon='lon2',lat=-10,lat=10)'
'dtadd2 = aave(dtadd,lon='lon3',lon='lon4',lat=-10,lat=10)'

'set display color white'; 'c'

'set t 0 39'
'set grads off'
'set grid off'
'set csmooth on'
cthick = '6'

'set parea 'panela; 'set vrange -0.3 2.4'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0.12'
'set cstyle 3'; 'set ccolor 1'; 'set cmark 0'; 'set cthick 'cthick; 'd dterai1'
'set cstyle 1'; 'set ccolor 4'; 'set cmark 0'; 'set cthick 'cthick; 'd dtctl1'
'set ccolor 8'; 'set cmark 0'; 'set cthick 'cthick; 'd dthtg1'
'set ccolor 15'; 'set cmark 0'; 'set cthick 1'; 'd dtadd1-dtadd1'
'set ccolor 15'; 'set cmark 0'; 'set cthick 1'; 'd dtadd1-dtadd1'
'set ccolor 3'; 'set cmark 0'; 'set cthick 'cthick; 'd dtadd1'

'set parea 'panelb; 'set vrange -0.3 2.4'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0.12'
'set cstyle 3'; 'set ccolor 1'; 'set cmark 0'; 'set cthick 'cthick; 'd dterai2'
'set cstyle 1'; 'set ccolor 4'; 'set cmark 0'; 'set cthick 'cthick; 'd dtctl2'
'set ccolor 8'; 'set cmark 0'; 'set cthick 'cthick; 'd dthtg2'
'set ccolor 15'; 'set cmark 0'; 'set cthick 1'; 'd dtadd2-dtadd2'
'set ccolor 3'; 'set cmark 0'; 'set cthick 'cthick; 'd dtadd2'


'set strsiz 0.13'; 'set string 1 l 4'
'draw string 0.55 8.35 g) E IO (80-110E,10S-10N)'
'draw string 5.75 8.35 h) W/C Pac (150E-150W,10S-10N)'

'set string 1 c 4'; 'draw string 3.2 5.6 ERA-Interim'
'set string 4 c 4'; 'draw string 4.7 5.6 Control'
'set string 8 c 4'; 'draw string 6.2 5.6 Added heating'
'set string 3 c 4'; 'draw string 8.2 5.6 directly added'

