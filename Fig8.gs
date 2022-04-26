
nskip = '2'

panela = '0.5 5.4 5.75 7.9'; panelb = '5.6 10.5 5.75 7.9'
panelc = '0.5 5.4 3.35 5.5'; paneld = '5.6 10.5 3.35 5.5'
panele = '0.5 5.4 0.95 3.1'; panelf = '5.6 10.5 0.95 3.1'

lon1 = 40; lon2 = 210
lat1 = -30; lat2 = 30

'reinit'
'sdfopen UV.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'set t 1 38'; 'u = Uobs'; 'v = Vobs'; 'set t 1'
'era1c = ave(u,t=1,t=38)'
'era2c = ave(v,t=1,t=38)'
'era12 = (u(t=1)+u(t=6)+u(t=8)+u(t=9)+u(t=14)+u(t=20))/6-era1c'
'era22 = (v(t=1)+v(t=6)+v(t=8)+v(t=9)+v(t=14)+v(t=20))/6-era2c'
'era11 = (u(t=16)+u(t=21)+u(t=25)+u(t=28)+u(t=29)+u(t=30)+u(t=33)+u(t=34)+u(t=35))/9-era1c'
'era21 = (v(t=16)+v(t=21)+v(t=25)+v(t=28)+v(t=29)+v(t=30)+v(t=33)+v(t=34)+v(t=35))/9-era2c'
'set t 1 38'; 'u = Uctl'; 'v = Vctl'; 'set t 1'
'mod1ca = ave(u,t=1,t=38)'
'mod2ca = ave(v,t=1,t=38)'
'mod12a = (u(t=1)+u(t=6)+u(t=8)+u(t=9)+u(t=14)+u(t=20))/6-mod1ca'
'mod22a = (v(t=1)+v(t=6)+v(t=8)+v(t=9)+v(t=14)+v(t=20))/6-mod2ca'
'mod11a = (u(t=16)+u(t=21)+u(t=25)+u(t=28)+u(t=29)+u(t=30)+u(t=33)+u(t=34)+u(t=35))/9-mod1ca'
'mod21a = (v(t=16)+v(t=21)+v(t=25)+v(t=28)+v(t=29)+v(t=30)+v(t=33)+v(t=34)+v(t=35))/9-mod2ca'
'set t 1 38'; 'u = Uhtg'; 'v = Vhtg'; 'set t 1'
'mod1cb = ave(u,t=1,t=38)'
'mod2cb = ave(v,t=1,t=38)'
'mod12b = (u(t=1)+u(t=6)+u(t=8)+u(t=9)+u(t=14)+u(t=20))/6-mod1cb'
'mod22b = (v(t=1)+v(t=6)+v(t=8)+v(t=9)+v(t=14)+v(t=20))/6-mod2cb'
'mod11b = (u(t=16)+u(t=21)+u(t=25)+u(t=28)+u(t=29)+u(t=30)+u(t=33)+u(t=34)+u(t=35))/9-mod1cb'
'mod21b = (v(t=16)+v(t=21)+v(t=25)+v(t=28)+v(t=29)+v(t=30)+v(t=33)+v(t=34)+v(t=35))/9-mod2cb'
'close 1'

'sdfopen DT.nc'
'set lon 'lon1' 'lon2
'set lat 'lat1' 'lat2
'set t 1 38'; 'dt = DTobs'; 'set t 1'
'qeraic = ave(dt,t=1,t=38)'
'qerai2 = (dt(t=1)+dt(t=6)+dt(t=8)+dt(t=9)+dt(t=14)+dt(t=20))/6-qeraic'
'qerai1 = (dt(t=16)+dt(t=21)+dt(t=25)+dt(t=28)+dt(t=29)+dt(t=30)+dt(t=33)+dt(t=34)+dt(t=35))/9-qeraic'
'set t 1 38'; 'dt = DTctl'; 'set t 1'
'qmodca = ave(dt,t=1,t=38)'
'qmod2a = (dt(t=1)+dt(t=6)+dt(t=8)+dt(t=9)+dt(t=14)+dt(t=20))/6-qmodca'
'qmod1a = (dt(t=16)+dt(t=21)+dt(t=25)+dt(t=28)+dt(t=29)+dt(t=30)+dt(t=33)+dt(t=34)+dt(t=35))/9-qmodca'
'set t 1 38'; 'dt = DThtg'; 'set t 1'
'qmodcb = ave(dt,t=1,t=38)'
'qmod2b = (dt(t=1)+dt(t=6)+dt(t=8)+dt(t=9)+dt(t=14)+dt(t=20))/6-qmodcb'
'qmod1b = (dt(t=16)+dt(t=21)+dt(t=25)+dt(t=28)+dt(t=29)+dt(t=30)+dt(t=33)+dt(t=34)+dt(t=35))/9-qmodcb'
'set t 1 38'; 'dt = DTadd'; 'set t 1'
'qaddc = ave(dt,t=1,t=38)'
'qadd2 = (dt(t=1)+dt(t=6)+dt(t=8)+dt(t=9)+dt(t=14)+dt(t=20))/6-qaddc'
'qadd1 = (dt(t=16)+dt(t=21)+dt(t=25)+dt(t=28)+dt(t=29)+dt(t=30)+dt(t=33)+dt(t=34)+dt(t=35))/9-qaddc'

** for 2*(20-1)=38 DOF
'tcrit = 2.024'

'set display color white'
'c'

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

*dark green
'set rgb 39  15 160  15'



'set grads off'
'set grid off'

'set parea 'panela
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set ylabs 30S||20S||10S||EQ||10N||20N||30N'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qmod1a'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(mod11a*mod11a+mod21a*mod21a)'
'd maskout(mod11a,mag-0.25);skip(mod21a,'nskip')'


'set parea 'panelb
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qmod2a'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(mod12a*mod12a+mod22a*mod22a)'
'd maskout(mod12a,mag-0.25);skip(mod22a,'nskip')'


'set parea 'panelc
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0.12'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qerai1'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(era11*era11+era21*era21)'
'd maskout(era11,mag-0.25);skip(era21,'nskip')'


'set parea 'paneld
'set gxout shaded'
'set xlopts 1 3 0'
'set ylopts 1 3 0'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qerai2'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(era12*era12+era22*era22)'
'd maskout(era12,mag-0.25);skip(era22,'nskip')'


'set parea 'panele
'set gxout shaded'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0.12'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qmod1b'
'set gxout contour'
'set clevs -0.45 -0.4 -0.35 -0.3 -0.25 -0.2 -0.15 -0.1 -0.05 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45'
'set ccolor 39'; 'set cthick 4'; 'set clab masked'
'd qadd1'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(mod11b*mod11b+mod21b*mod21b)'
'd maskout(mod11b,mag-0.25);skip(mod21b,'nskip')'


'set parea 'panelf
'set gxout shaded'
'set xlopts 1 3 0.12'
'set ylopts 1 3 0'
'set clevs -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9'
'set ccols 49 48 47 46 45 44 43 42 41 0 21 22 23 24 25 26 27 28 29'
'd qmod2b'
'set gxout contour'
'set clevs -0.45 -0.4 -0.35 -0.3 -0.25 -0.2 -0.15 -0.1 -0.05 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45'
'set ccolor 39'; 'set cthick 4'; 'set clab masked'
'd qadd2'
'set arrscl 0.15 0.75'
'set arrlab off'
'set cthick 1'
'set ccolor 1'
'mag = sqrt(mod12b*mod12b+mod22b*mod22b)'
'd maskout(mod12b,mag-0.25);skip(mod22b,'nskip')'


'cbarn.gs 0.7 0 3.25 0.4 1'
rc = arrow(7.75,0.4,0.3,1.5,1,1)

'set strsiz 0.13'; 'set string 1 l 4'
'draw string 0.55 8   a) Control';      'draw string 5.65 8    b) Control'
'draw string 0.55 5.6 c) ERA-Interim';  'draw string 5.65 5.6  d) ERA-Interim'
'draw string 0.55 3.2 e) Added heating'; 'draw string 5.65 3.2 f) Added heating'

'set strsiz 0.13'; 'set string 1 r 4'
'draw string 5.35 8    0.0, +0.1'; 'draw string 10.45 8   +0.4,  0.0'
'draw string 5.35 5.6 +1.5, +1.5'; 'draw string 10.45 5.6 -1.3, -1.3'
'draw string 5.35 3.2 +1.3, +0.4'; 'draw string 10.45 3.2 -1.0, -0.3'

'set strsiz 0.16'
'set string 39 r 4'
'draw string 10.7 0.4 directly added'

'set string 1 c 5'
'draw string 2.95 8.3 EQUINOO (+)'
'draw string 8.05 8.3 EQUINOO (-)'


'set string 1 c 4'
'set strsiz 0.13'
'draw string 6.75 0.25 K/day'
'draw string 8.25 0.25 m/s'

function arrow(x,y,len,scale,thick,col)
'set line 'col' 1 'thick
'draw line 'x-len/2.' 'y' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y+0.025' 'x+len/2.' 'y
'draw line 'x+len/2.-0.05' 'y-0.025' 'x+len/2.' 'y
'set string 'col' c'
'set strsiz 0.15'
'draw string 'x' 'y-0.15' 'scale
return

