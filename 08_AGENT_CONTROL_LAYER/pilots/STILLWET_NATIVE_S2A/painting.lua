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
