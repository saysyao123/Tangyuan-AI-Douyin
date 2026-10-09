-- S2A GPT painter | Brief: white porcelain cup, lemon, warm grey linen | no source image
-- Real painter decision: warm-dark olive backdrop, cold ivory cup, single luminous lemon.
-- Every chunk is a genuinely executable easel step; revision requires looking at actual output.
--@ box giverny
--@ engine 4

--@ chunk 1
canvas{size=460, aspect=0.8, linen={18,16}, seed=2409,
  ground={{pile={{"lead white",9},{"yellow ochre",0.45},{"cobalt violet",0.22}},um=110,apply="brush",texture=0.10}}}
-- Keep regions as meaningful shapes to paint, NOT pixels from a reference image.
backM=rect(0,0,1000,785)
tableM=rect(0,785,1000,465)
cupBody=poly({{435,458},{678,458},{681,556},{674,726},{655,837},{624,890},{485,892},{448,836},{439,717}},true)
cupHandle=ellipse(725,650,94,136)-ellipse(744,650,54,90)
cupRim=ellipse(557,462,124,34)
cupM=cupBody+cupHandle+cupRim
lemonM=ellipse(296,906,141,91)
lemonTip=ellipse(431,902,24,23)
lemonAll=lemonM+lemonTip

-- The still-life starts with deliberate graphite construction.
pencil1=pencil("2H")
pencil1:sketch({{0,783},{290,783},{530,784},{760,783},{1000,782}},{pressure=0.27,passes=2})
pencil1:sketch({{435,457},{434,538},{442,720},{449,818},{484,890},{555,902},{622,890},{657,830},{680,717},{682,565},{678,458}},{pressure=0.32})
pencil1:sketch({{434,460},{483,436},{558,431},{631,440},{680,461},{634,482},{559,495},{488,483},{434,460}},{pressure=0.25})
pencil1:sketch({{664,556},{739,520},{806,571},{814,659},{774,744},{694,752}},{pressure=0.28})
pencil1:sketch({{155,910},{195,837},{302,816},{387,845},{439,900},{390,959},{298,993},{209,976},{155,910}},{pressure=0.35})
fix()
bg1=pile({{"ultramarine blue",2},{"carmine lake",1.15},{"viridian",0.55},{"yellow ochre",0.45},{"lead white",1.2},turps=0.35})
bg2=pile({{"ultramarine blue",0.8},{"carmine lake",0.55},{"yellow ochre",1.4},{"lead white",5},turps=0.3})
work(backM,{hand="broad",pile=bg1,coverage=1.55,angle=0.18,length={65,160},tool="filbert 24",edge="soft",fill=true,seed=211})
work(tableM,{hand="broad",pile=bg2,coverage=1.7,angle=0.04,length={70,190},tool="filbert 22",fill=true,seed=212})
-- The following are thin, purposely imperfect first layers.
cupBase=pile({{"lead white",8},{"yellow ochre",0.28},{"cobalt blue",0.32},{"cobalt violet",0.1},turps=0.28})
lemonBase=pile({{"cadmium yellow",2.0},{"yellow ochre",1.4},{"lead white",0.95},{"carmine lake",0.13},turps=0.28})
work(cupHandle,{hand="body",pile=cupBase,coverage=1.5,angle=1.57,tool="filbert 13",length={18,55},fill=true,seed=214})
work(cupBody,{hand="body",pile=cupBase,coverage=1.8,angle=1.5,tool="filbert 15",length={25,75},fill=true,seed=215})
work(lemonAll,{hand="body",pile=lemonBase,coverage=1.8,angle=0.15,tool="filbert 13",length={18,55},fill=true,seed=216})
print("GPT painter S2A stage 1: compositional graphite, broad lay-in; look before planning next pass")


--@ chunk 2
-- GPT LOOK 01 (real 600x750 canvas): background unexpectedly purple, cup streaky,
-- lemon flat. Rebalance color masses and build volumes; not a scripted next step.
wait(24*60)
protectObjects=(cupM+lemonAll):grow(9)
neutralBackdrop=pile({{"yellow ochre",3.0},{"viridian",0.9},{"ultramarine blue",0.35},{"carmine lake",0.28},{"lead white",1.05}})
neutralCloth=pile({{"lead white",6},{"yellow ochre",1.2},{"cobalt blue",0.52},{"viridian",0.12},{"carmine lake",0.14}})
shadowPaint=pile({{"ultramarine blue",1.05},{"carmine lake",0.42},{"yellow ochre",0.60},{"lead white",1.7}})
work(backM-protectObjects,{hand="body",tool="filbert 18",pile=neutralBackdrop,coverage=2.1,load=0.68,length={40,115},angle=0.14,edge="soft",fill=true,seed=301})
work(tableM-protectObjects,{hand="body",tool="filbert 16",pile=neutralCloth,coverage=1.8,load=0.63,length={45,120},angle=0.0,edge="soft",fill=true,seed=302})
work(ellipse(557,902,215,48):soften(27),{hand="scumble",tool="filbert 14",pile=shadowPaint,coverage=1.3,load=0.3,angle=0,seed=303})
work(ellipse(295,967,166,42):soften(18),{hand="scumble",tool="filbert 12",pile=shadowPaint,coverage=1.2,load=0.32,angle=0,seed=304})

-- Reunify the cup into a solid porcelain volume using small vertical marks.
ivoryMid=pile({{"lead white",16},{"yellow ochre",0.35},{"cobalt blue",0.30}})
ivoryDark=pile({{"lead white",5},{"cobalt blue",1.1},{"cobalt violet",0.25},{"yellow ochre",0.35}})
ivoryLit=pile({{"lead white",23},{"yellow ochre",0.16}})
work(cupHandle,{hand="body",tool="filbert 8",pile=ivoryDark,coverage=2.5,angle=1.5,length={13,40},fill=true,clip=true,seed=305})
work(cupBody,{hand="body",tool="filbert 8",pile=ivoryMid,coverage=3.2,angle=1.52,length={12,38},fill=true,clip=true,seed=306})
work(cupBody*rect(584,465,115,445):soften(62),{hand="body",tool="filbert 6",pile=ivoryDark,coverage=1.95,angle=1.50,length={10,28},clip=true,seed=307})
work(cupBody*rect(449,471,122,385):soften(55),{hand="body",tool="filbert 6",pile=ivoryLit,coverage=2.0,angle=1.55,length={12,30},clip=true,seed=308})

-- A visible elliptical mouth gives the viewer an unambiguous cup rather than a cylinder.
rimInner=ellipse(557,461,113,25)
rimOuter=ellipse(557,462,126,35)
rimRing=rimOuter-rimInner
work(rimInner,{hand="body",tool="filbert 5",pile=ivoryDark,coverage=3.0,angle=0,length={10,26},fill=true,clip=true,seed=309})
work(rimRing,{hand="body",tool="filbert 4",pile=ivoryLit,coverage=3.8,angle=0,length={8,20},fill=true,clip=true,seed=310})

-- Deliberate lemon modeling: darker lower-right, sunward upper-left.
lemonShade=pile({{"cadmium yellow",2},{"yellow ochre",1.6},{"viridian",0.43},{"carmine lake",0.16}})
lemonLit=pile({{"cadmium yellow",2.7},{"lead white",1.6},{"barium yellow",0.55}})
work(lemonM*ellipse(334,944,134,73):soften(45),{hand="body",tool="filbert 7",pile=lemonShade,coverage=2.0,angle=0.3,length={10,35},clip=true,seed=311})
work(lemonM*ellipse(253,860,135,75):soften(43),{hand="body",tool="filbert 6",pile=lemonLit,coverage=2.2,angle=0.2,length={11,30},clip=true,seed=312})
print("GPT painter S2A stage 2: after LOOK 01, warm background, shaped cup, visible rim, modelled lemon")
