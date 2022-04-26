
clevs1 = '0.4 0.8 1.2 1.6 2 2.4 2.8 3.2 3.6'
clevs2 = '-1.8 -1.6 -1.4 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0.2 0.4 0.6 0.8 1 1.2 1.4 1.6 1.8'
clevs3 = '-3.6 -3.2 -2.8 -2.4 -2 -1.6 -1.2 -0.8 -0.4 0.4 0.8 1.2 1.6 2 2.4 2.8 3.2 3.6'
clevs4 = '0.8 1.6 2.4 3.2 4.0 4.8 5.6'

panela = '0.5 5.4 5.75 7.9'; panelb = '5.6 10.5 5.75 7.9'
panelc = '0.5 5.4 3.35 5.5'; paneld = '5.6 10.5 3.35 5.5'
panele = '0.5 5.4 0.95 3.1'; panelf = '5.6 10.5 0.95 3.1'

lon1 = 40; lon2 = 210
lat1 = -30; lat2 = 30

'reinit'
'sdfopen DT.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'dteraim = ave(dtobs,t=1,t=38)'
'dteraiv = ave((dtobs-dteraim)*(dtobs-dteraim),t=1,t=38)'
'dtmod1m = ave(dtctl,t=1,t=38)'
'dtmod1v = ave((dtctl-dtmod1m)*(dtctl-dtmod1m),t=1,t=38)'
'dtmod2m = ave(dthtg,t=1,t=38)'
'dtmod2v = ave((dthtg-dtmod2m)*(dthtg-dtmod2m),t=1,t=38)'
'dtadd = ave(dtadd,t=1,t=38)'

** for 2*(38-1)=74 DOF
'tcrit = 1.993'

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

'set grads off'
'set grid off'
'set csmooth on'

'var1 = dtmod1m-dteraim'
'sigpool=sqrt((38*dtmod1v+38*dteraiv)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'panelb
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set ylabs 30S||20S||10S||EQ||10N||20N||30N'
'set clevs 'clevs2
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd vart1'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs3
'd vart1'

'set parea 'panela
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set clevs 'clevs1
'set ccols 0 21 22 23 24 25 26 27 28 29'
'd dtmod1m'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd dtmod1m'

'var1 = dtmod2m-dtmod1m'
'sigpool=sqrt((38*dtmod2v+38*dtmod1v)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'paneld
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set ylabs 30S||20S||10S||EQ||10N||20N||30N'
'set clevs 'clevs2
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd vart1'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs3
'd var1'
'set gxout contour'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccolor 39'; 'set cthick 4'; 'set clab masked'
'd dtadd'

'set parea 'panelc
'set gxout shaded'
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set clevs 'clevs1
'set ccols 0 21 22 23 24 25 26 27 28 29'
'd dteraim'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd dteraim'

'var1 = dtmod2m-dteraim'
'sigpool=sqrt((38*dtmod2v+38*dteraiv)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'panelf
'set gxout shaded'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0'
'set ylabs 30S||20S||10S||EQ||10N||20N||30N'
'set clevs 'clevs2
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd vart1'
'cbarn.gs 0.45 0 8.05 0.4 1'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs3
'd var1'

'set parea 'panele
'set gxout shaded'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0.12'
'set clevs 'clevs1
'set ccols 0 21 22 23 24 25 26 27 28 29'
'd dtmod2m'
'cbarn.gs 0.45 0 2.95 0.4 0'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd dtmod2m'

'set strsiz 0.13'; 'set string 1 l 4'
'draw string 0.55 8   a) Control';      'draw string 5.65 8    b) Control minus ERA-Interim'
'draw string 0.55 5.6 c) ERA-Interim';  'draw string 5.65 5.6  d) Added heating minus Control'
'draw string 0.55 3.2 e) Added heating'; 'draw string 5.65 3.2 f) Added heating minus ERA-Interim'

'set strsiz 0.13'
'set string 39 l 4'
'draw string 6 3.55 directly added'

'set string 1 c 4'
'set strsiz 0.13'
'draw string 5.5 0.25 K/day'
