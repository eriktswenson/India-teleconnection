
clevs1 = '2 4 6 8 10 12 14 16 18'
clevs2 = '-8 -7 -6 -5 -4 -3 -2 -1 1 2 3 4 5 6 7 8'
clevs3 = '-8 -6 -4 -2 2 4 6 8'
clevs4 = '4 8 12 16'

panela = '0.5 5.4 5.75 7.9'; panelb = '5.6 10.5 5.75 7.9'
panelc = '0.5 5.4 3.35 5.5'; paneld = '5.6 10.5 3.35 5.5'
panele = '0.5 5.4 0.95 3.1'; panelf = '5.6 10.5 0.95 3.1'

lon1 = 40; lon2 = 210
lat1 = -20; lat2 = 40

'reinit'
'sdfopen PREC.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'pobs = gpcp(t=1)'
'pobsvar = gpcp(t=2)'
'pctl = ctl(t=1)'
'pctlvar = ctl(t=2)'
'phtg = htg(t=1)'
'phtgvar = htg(t=2)'

** for 2*(38-1)=74 DOF
'tcrit = 1.993'

'set display color white'; 'c'

*light green -> dark green; light purple -> dark purple
'set rgb 31 230 255 225'; 'set rgb 51 220 220 255'
'set rgb 32 200 255 190'; 'set rgb 52 192 180 255'
'set rgb 33 180 250 170'; 'set rgb 53 160 140 255'
'set rgb 34 150 245 140'; 'set rgb 54 128 112 235'
'set rgb 35 120 245 115'; 'set rgb 55 112  96 220'
'set rgb 36  80 240  80'; 'set rgb 56  72  60 200'
'set rgb 37  55 210  60'; 'set rgb 57  60  40 180'
'set rgb 38  30 180  30'; 'set rgb 58  45  30 165'
'set rgb 39  15 160  15'; 'set rgb 59  40   0 160'

'set grads off'
'set grid off'
'set csmooth on'

'var1 = pctl-pobs'
'sigpool=sqrt((38*pctlvar+38*pobsvar)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'panelb
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set ylabs 20S||10S||EQ||10N||20N||30N||40N'
'set clevs 'clevs2
'set ccols 59 58 57 56 55 54 53 52 0 32 33 34 35 36 37 38 39'
'd vart1'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs3
'd var1'

'set parea 'panela
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set clevs 'clevs1
'set ccols 0 31 32 33 34 35 36 37 38 39'
'd pctl'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd pctl'

'var1 = phtg-pctl'
'sigpool=sqrt((38*phtgvar+38*pctlvar)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'paneld
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set ylabs 20S||10S||EQ||10N||20N||30N||40N'
'set clevs 'clevs2
'set ccols 59 58 57 56 55 54 53 52 0 32 33 34 35 36 37 38 39'
'd vart1'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs3
'd var1'

'set parea 'panelc
'set gxout shaded'
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set clevs 'clevs1
'set ccols 0 31 32 33 34 35 36 37 38 39'
'd pobs'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd pobs'

'var1 = phtg-pobs'
'sigpool=sqrt((38*phtgvar+38*pobsvar)/74)'
't1=var1/(sigpool*sqrt(1/38+1/38))'
'vart1 = maskout(var1,abs(t1)-tcrit)'

'set parea 'panelf
'set gxout shaded'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0'
'set ylabs 20S||10S||EQ||10N||20N||30N||40N'
'set clevs 'clevs2
'set ccols 59 58 57 56 55 54 53 52 0 32 33 34 35 36 37 38 39'
'd vart1'
'cbarn.gs 0.45 0 8.05 0.4 0'
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
'set ccols 0 31 32 33 34 35 36 37 38 39'
'd phtg'
'cbarn.gs 0.45 0 2.95 0.4 0'
'set gxout contour'
'set ccolor 15'; 'set cthick 1'
'set clab off'
'set clevs 'clevs4
'd phtg'

'set strsiz 0.13'; 'set string 1 l 4'
'draw string 0.55 8   a) Control';      'draw string 5.65 8    b) Control minus GPCP'
'draw string 0.55 5.6 c) GPCP';  'draw string 5.65 5.6  d) Added heating minus Control'
'draw string 0.55 3.2 e) Added heating'; 'draw string 5.65 3.2 f) Added heating minus GPCP'

'set string 1 c 4'
'set strsiz 0.13'
'draw string 5.5 0.25 mm/day'

