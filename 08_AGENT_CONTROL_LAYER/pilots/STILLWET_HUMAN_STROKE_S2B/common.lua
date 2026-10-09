-- Alice's Stillwet actual Rust engine | S2B shared substrate | original GPT instructions
--@ box giverny
--@ engine 4
--@ chunk 1
canvas{size=480, aspect=0.8, linen={17,16}, seed=422,
  ground={{pile={{"lead white",8},{"yellow ochre",0.52},{"cobalt violet",0.10}},um=105,apply="brush",texture=0.10}}}
wall=rect(0,0,1000,815)
tableTop=rect(0,815,1000,435)
cup=poly({{481,493},{709,493},{711,577},{702,754},{674,886},{635,936},{543,939},{501,898},{479,768}},true)
handle=ellipse(750,683,86,128)-ellipse(756,684,54,95)
rimOuter=ellipse(594,497,119,35)
rimInside=ellipse(594,498,107,25)
lemon=ellipse(307,965,139,83)
lemonTip=ellipse(443,965,20,17)
objs=cup+handle+rimOuter+lemon+lemonTip
bg=pile({{"ultramarine blue",1.7},{"yellow ochre",1.1},{"viridian",0.38},{"carmine lake",0.23},{"lead white",1.6},turps=0.28})
cloth=pile({{"lead white",7},{"yellow ochre",1.05},{"cobalt blue",0.34},{"carmine lake",0.13},turps=0.22})
white=pile({{"lead white",17},{"yellow ochre",0.20},{"cobalt blue",0.22}})
cool=pile({{"lead white",6},{"cobalt blue",0.78},{"cobalt violet",0.25}})
warmwhite=pile({{"lead white",18},{"yellow ochre",0.57}})
yellow=pile({{"cadmium yellow",2},{"yellow ochre",0.6},{"lead white",0.65}})
sun=pile({{"cadmium yellow",2},{"barium yellow",0.95},{"lead white",1.60}})
darklemon=pile({{"yellow ochre",1.6},{"cadmium yellow",0.8},{"viridian",0.28}})
shade=pile({{"ultramarine blue",0.9},{"yellow ochre",0.8},{"lead white",1.4}})
-- Both lanes share IDENTICAL preliminary broad drawing / first touch.
p=pencil("2H")
p:sketch({{0,813},{400,813},{1000,813}},{pressure=0.2})
p:sketch({{481,493},{478,739},{502,888},{542,938},{638,938},{677,881},{709,577},{709,493}},{pressure=0.25})
p:sketch({{170,966},{217,902},{309,884},{388,907},{446,966},{401,1022},{305,1048},{207,1030},{170,966}},{pressure=0.23})
fix()
-- S2B2: the shared PRIMARY underpainting itself must not become wallpaper.
-- Intentional long, varied, fully covered broad passages followed by soft blending.
work(wall-objs:grow(12),{hand="broad",pile=bg,coverage=2.15,
  angle=function(x,y) return 0.12+0.24*math.sin(y/218) end,
  angle_jitter=0.22,curve={0.20,0.11},length={95,195},
  load=0.63,dips={3,0.72,0.92},fill=true,clip=true,seed=100})
blend(wall-objs:grow(12),{angle=0.20,coverage=0.63,clip=true,seed=105})
work(tableTop-objs:grow(6),{hand="broad",pile=cloth,coverage=2.0,
  angle=function(x,y) return 0.06+0.14*math.sin(x/188) end,
  angle_jitter=0.17,curve={0.12,0.07},length={90,170},
  load=0.63,fill=true,clip=true,seed=101})
blend(tableTop-objs:grow(6),{angle=0.03,coverage=0.45,clip=true,seed=106})
work(ellipse(596,942,192,30):soften(12),{hand="scumble",pile=shade,coverage=0.75,angle=0,clip=true,seed=102})
work(ellipse(321,1041,160,20):soften(12),{hand="scumble",pile=shade,coverage=0.7,angle=0,clip=true,seed=103})
print("S2B identical first ground; separate A/B painter decisions follow")
