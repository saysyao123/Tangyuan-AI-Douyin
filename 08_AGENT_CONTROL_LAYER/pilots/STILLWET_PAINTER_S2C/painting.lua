-- Stillwet S2C v1: original GPT-designed still life. No image-to-video / sampled source image.
-- Method follows documented original studio practice, not replay of an archived painting.
--@ engine 4
--@ chunk 1
canvas{size=460, aspect=1.25, linen={17,13}, seed=2609, ground={
 {pile={{"lead white",1}},um=100,apply="knife",texture=0.27},
 {pile={{"lead white",3.1},{"yellow ochre",0.75},{"raw umber",0.65}},um=24,apply="brush",texture=0.17}
}}
print("S2C: Chardin-inspired quiet earth palette, upper-left diffuse daylight")

--@ chunk 2
-- A wider-bellied stoneware jug at x375 with two overlapping lemons and a small worn iron knife.
g=chalk()
g:sketch({{0,532},{230,532},{560,533},{1000,532}},{pressure=0.28})
g:sketch({{0,694},{300,694},{700,695},{1000,696}},{pressure=0.21})
g:sketch({{303,221},{275,287},{245,386},{251,481},{291,561},{340,601},{424,608},{478,565},{507,476},{503,377},{470,288},{438,223}},{pressure=0.35})
g:sketch({{303,221},{337,200},{370,196},{412,203},{438,223},{411,241},{375,248},{330,241},{303,221}},{pressure=0.28})
g:sketch({{435,267},{505,258},{550,304},{551,382},{511,431},{484,439}},{pressure=0.25})
g:sketch({{547,595},{570,556},{628,548},{685,566},{707,616},{676,653},{618,662},{559,640},{547,595}},{pressure=0.25})
g:sketch({{688,562},{711,533},{750,521},{810,540},{838,570},{806,597},{751,608},{707,596}},{pressure=0.23})
g:sketch({{665,672},{739,679},{820,703},{910,740}},{pressure=0.16})

-- Geometry is only a guide; later passages must use lost edges, not crisp clipping.
jugBody=poly({{307,222},{286,288},{257,358},{244,416},{253,481},{284,549},{329,588},{377,608},{421,602},{465,580},{491,530},{506,465},{503,397},{487,324},{458,262},{437,222}},true)
rim=ellipse(371,217,68,22)
neck=rect(306,207,133,60):soften(18)
handle=ribbon({{442,273},{503,269},{548,308},{553,380},{518,420},{489,433}}, {22,21,18,17,15,13})
jug=jugBody+rim+handle
lem1=ellipse(628,607,79,53)
lem2=ellipse(761,567,77,46)
lemons=lem1+lem2
wall=rect(0,0,1000,534)
ledge=rect(0,534,1000,160)
ledgeFace=rect(0,694,1000,106)
print("S2C: hand-planned jug contour, two overlapping lemons, ledge with cast-light from upper left")

--@ chunk 3
-- A quiet, atmospheric wall: not full digital coverage, subtly varying warm umber shadow.
wDark=pile{{"raw umber",3.0},{"bone black",0.83},{"red earth",0.32},{"lead white",0.31},medium=0.12}
wOlive=pile{{"raw umber",2.25},{"green earth",0.78},{"yellow ochre",0.88},{"bone black",0.48},{"lead white",1.1},medium=0.10}
wSoft=pile{{"raw umber",1.65},{"yellow ochre",0.77},{"green earth",0.47},{"lead white",1.65},{"bone black",0.16},medium=0.13}
local protected=(jug+lemons):grow(7)
local p=wall-protected
work(p,{hand="broad",pile=wDark,coverage=1.92,angle=function(x,y) return 0.65+0.21*math.sin(x/230+y/190) end,angle_jitter=0.23,edge="soft",length={65,145},fill=true,seed=103})
work(p,{hand="body",tool="filbert 13",pile=wOlive,coverage=1.15,angle=function(x,y) return 0.91+0.17*math.sin(x/184) end,angle_jitter=0.17,edge="soft",length={28,65},seed=104})
local lit=mask(function(x,y) local dx=(x-745)/450 local dy=(y-300)/420 return math.max(0,math.min(1,1.1-math.sqrt(dx*dx+dy*dy))) end)*p
work(lit,{hand="scumble",tool="filbert 16",pile=wSoft,coverage=0.88,threshold=0.28,edge="lost",seed=105})
blend(p,{angle=0.71,tool={kind="badger",width=30}})
print("S2C: wall dark and living in air, deliberately not uniformly flat")

--@ chunk 4
tTop=pile{{"lead white",2.4},{"yellow ochre",1.13},{"raw umber",1.48},{"bone black",0.21}}
tBack=pile{{"raw umber",1.7},{"bone black",0.37},{"yellow ochre",0.49},{"lead white",0.56}}
tFront=pile{{"raw umber",2.9},{"yellow ochre",0.61},{"bone black",0.91},{"lead white",0.4}}
local m=ledge-(jug+lemons):grow(6)
work(m,{hand="broad",tool="filbert 14",pile=tTop,coverage=1.7,angle=0.06,angle_jitter=0.15,length={43,98},edge="firm",fill=true,seed=111})
work(m*rect(0,530,1000,49):soften(24),{hand="body",tool="filbert 10",pile=tBack,coverage=0.87,angle=0.04,edge="soft",seed=112})
work(ledgeFace,{hand="body",tool="filbert 13",pile=tFront,coverage=1.80,angle=0.05,angle_jitter=0.11,length={42,115},edge="firm",fill=true,seed=113})
blend(ledge-(jug+lemons):grow(5),{angle=0.06,tool={kind="badger",width=24}})
print("S2C: soft stone ledge and front plane")


--@ chunk 5
-- GPT LOOK 01: background air present, table reads as stone, forms left unpainted.
-- Block subject with earth-pigment values while preserving a hand-made edge.
jWarm=pile{{"lead white",5.6},{"yellow ochre",0.57},{"raw umber",0.38},{"green earth",0.16}}
jLight=pile{{"lead white",8.2},{"yellow ochre",0.49},{"raw umber",0.09}}
jHalf=pile{{"lead white",3.15},{"yellow ochre",0.73},{"raw umber",0.80},{"green earth",0.32}}
jOpening=pile{{"raw umber",1.85},{"bone black",0.68},{"green earth",0.23},{"lead white",0.55}}
lemonMid=pile{{"chrome yellow",2.0},{"yellow ochre",0.88},{"lead white",0.56}}
lemonBack=pile{{"chrome yellow",1.22},{"yellow ochre",1.26},{"raw umber",0.45},{"green earth",0.28}}
work(handle,{hand="body",tool="filbert 9",pile=jHalf,coverage=1.7,angle=1.44,angle_jitter=0.16,curve={0.17,0.07},length={16,43},edge="firm",seed=151})
work(jugBody,{hand="body",tool="filbert 13",pile=jWarm,coverage=2.25,angle=0.12,angle_jitter=0.20,curve={0.25,0.12},length={24,63},edge="firm",fill=true,seed=152})
-- Broad light is only left-half and upper shoulder, with a soft lost edge.
local jl=jugBody*mask(function(x,y) return smoothstep(410,320,x)*smoothstep(594,482,y) end)
work(jl,{hand="scumble",tool="filbert 11",pile=jLight,coverage=1.42,angle=0.11,edge="soft",load=0.58,seed=153})
work(lem2,{hand="body",tool="filbert 10",pile=lemonBack,coverage=2.35,angle=0.03,angle_jitter=0.16,curve={0.20,0.08},fill=true,edge="firm",seed=154})
work(lem1,{hand="body",tool="filbert 10",pile=lemonMid,coverage=2.35,angle=-0.13,angle_jitter=0.15,curve={0.21,0.06},fill=true,edge="firm",seed=155})
work(rim,{hand="body",tool="filbert 5",pile=jHalf,coverage=1.65,angle=0.04,length={10,25},edge="firm",seed=156})
print("S2C: jug and fruit body colour, no uniform white silhouette")

--@ chunk 6
-- A genuine dry painting stage (not waiting real-world wall-clock time).
print("before dry",drying(365,424),drying(630,610),drying(80,80))
print(wait(4*24*60))
print("after dry",drying(365,424),drying(630,610),drying(80,80))

--@ chunk 7
-- Transparent shadow veil over DRY light stoneware. No white pigment in glaze.
jGlaze=pile{{"raw umber",2.2},{"green earth",0.88},{"bone black",0.39},{"yellow ochre",0.35},medium=0.88}
jGlazeDeep=pile{{"raw umber",2.10},{"bone black",0.75},{"green earth",0.37},medium=0.86}
jugShade=jugBody*mask(function(x,y)
 local t=(x-246)/265
 return smoothstep(0.36,0.81,t)*smoothstep(250,319,y)
end)
jugCore=jugBody*mask(function(x,y)
 local t=(x-246)/265
 return smoothstep(0.66,0.92,t)*smoothstep(270,330,y)
end)
work(jugShade,{hand="glaze",tool="filbert 17",pile=jGlaze,coverage=1.62,angle=1.51,length={35,85},load=0.35,clip=jugShade,threshold=0.30,seed=171})
work(jugCore,{hand="glaze",tool="filbert 12",pile=jGlazeDeep,coverage=0.83,angle=1.50,length={24,73},load=0.31,clip=jugCore,threshold=0.32,seed=172})
-- Lid aperture: narrow warm grey inner plane, rim left side bright.
work(ellipse(373,213,58,13),{hand="body",tool="filbert 5",pile=jOpening,coverage=2.2,angle=0,length={10,22},clip=true,seed=173})
rimHighlight=pile{{"lead white",7.5},{"yellow ochre",0.30},{"raw umber",0.05}}
b=brush("filbert",4)
b:reload(rimHighlight,0.77)
b:stroke({{306,220},{337,234},{374,236},{410,229},{435,219}},{pressure={0.64,0.13},ramps={0.12,0.33}})
print("S2C: transparent earth glazes sculpt pale dry jug, purposeful rim structure")

--@ chunk 8
-- The lemons are painted by groups of short curved strokes of changing hue.
-- No global badger blend on fruits; preserve directional, tactile fruit marks.
lemonDeep=pile{{"yellow ochre",2.0},{"raw umber",0.72},{"green earth",0.51},{"chrome yellow",0.63}}
lemonWarm=pile{{"chrome yellow",2.0},{"yellow ochre",1.10},{"lead white",0.40}}
lemonSun=pile{{"chrome yellow",1.84},{"lead white",2.2},{"yellow ochre",0.17}}
lShade1=lem1*ellipse(669,638,80,48):soften(18)
lShade2=lem2*ellipse(806,594,74,40):soften(18)
lBright1=lem1*ellipse(594,578,71,45):soften(21)
lBright2=lem2*ellipse(730,543,74,38):soften(22)
work(lShade2,{hand="body",tool="filbert 6",pile=lemonDeep,coverage=1.45,angle=0.30,length={10,24},edge="soft",seed=181})
work(lShade1,{hand="body",tool="filbert 6",pile=lemonDeep,coverage=1.45,angle=0.21,length={11,26},edge="soft",seed=182})
work(lBright2,{hand="body",tool="filbert 5",pile=lemonSun,coverage=1.35,angle=-0.21,length={9,22},edge="soft",seed=183})
work(lBright1,{hand="body",tool="filbert 5",pile=lemonSun,coverage=1.39,angle=-0.28,length={10,24},edge="soft",seed=184})
fruitBrush=brush("filbert",6)
for i=0,4 do
  local yy=572+i*13
  fruitBrush:reload(lemonWarm,0.62)
  fruitBrush:stroke({{570,yy+12},{604,yy+3},{641,yy+2},{668,yy+12}},{pressure={0.52,0.12},ramps={0.12,0.27},clip=lem1})
end
for i=0,3 do
  local yy=537+i*13
  fruitBrush:reload(lemonWarm,0.58)
  fruitBrush:stroke({{708,yy+13},{739,yy+2},{773,yy+5},{808,yy+16}},{pressure={0.51,0.13},ramps={0.14,0.30},clip=lem2})
end
print("S2C: distinct dark, middle and light form notes on fruit; no flat yellow blocks")


--@ chunk 9
-- GPT LOOK 02: a very specific failure, as in original r16 journal:
-- deep umber glaze at 1.62 coverage on setting white forms irregular black islands.
-- No pretending this is improved; let it actually DRY before repairing tonality.
print("LOOK02 before waiting",drying(430,405),drying(484,462),drying(629,615))
print(wait(6*24*60))
print("LOOK02 after waiting",drying(430,405),drying(484,462),drying(629,615))

--@ chunk 10
-- Redesign the jug from VALUE/FORM, not outline. Opaque midtones veil failed black islands,
-- preserving some irregular salt-glaze variation under the paint.
jRestoreLit=pile{{"lead white",7.4},{"yellow ochre",0.50},{"raw umber",0.14}}
jRestoreHalf=pile{{"lead white",3.15},{"yellow ochre",0.55},{"raw umber",0.83},{"green earth",0.33}}
jRestoreCore=pile{{"lead white",1.55},{"raw umber",1.12},{"green earth",0.51},{"bone black",0.13},{"yellow ochre",0.36}}
-- Graded mixtures at each brush DIP, rather than mask-banded bands of opaque colors.
work(jugBody,{hand="body",tool="filbert 13",coverage=2.25,angle=function(x,y) return 0.12+0.12*math.sin(y/190) end,
 angle_jitter=0.21,curve={0.24,0.11},length={22,63},load=0.59,edge="soft",fill=true,clip=true,seed=210,
 piles={
 {jRestoreLit,function(x,y) return 1.0-smoothstep(310,475,x) end},
 {jRestoreHalf,function(x,y) return 0.22+0.61*smoothstep(315,463,x) end},
 {jRestoreCore,function(x,y) return 0.88*smoothstep(375,505,x) end}
 }})
-- Restrained clean badger on SHADOW HALF only: never drag dark across the light.
local sh=jugBody*mask(function(x,y) return smoothstep(375,457,x)*smoothstep(255,321,y) end)
blend(sh,{angle=1.47,tool={kind="badger",width=18},clip=true})
print("S2C: restored value turning with graded piles; former dark glaze now controlled underpaint")

--@ chunk 11
-- Small shape-read corrections instead of another global wash.
print(wait(4*24*60))
print("dryness after repair",drying(368,409),drying(461,423))
jSideGlow=pile{{"lead white",4.4},{"raw umber",0.76},{"yellow ochre",0.55},{"green earth",0.26}}
jLightAccent=pile{{"lead white",6.0},{"yellow ochre",0.40}}
local refl=jugBody*mask(function(x,y) return smoothstep(432,495,x)*smoothstep(455,532,y)*smoothstep(578,524,y) end)
work(refl,{hand="scumble",tool="filbert 8",pile=jSideGlow,coverage=0.71,load=0.33,angle=1.6,length={16,38},clip=jugBody,edge="soft",seed=220})
local upperLight=jugBody*mask(function(x,y) return (1-smoothstep(301,365,x))*(1-smoothstep(310,446,y)) end)
work(upperLight,{hand="scumble",tool="filbert 6",pile=jLightAccent,coverage=0.51,load=0.26,angle=1.1,length={13,30},edge="soft",seed=221})
-- Jug handle: the interior should read as opening, not scattered marks.
handleShadow=pile{{"raw umber",2.1},{"bone black",0.65},{"green earth",0.18},{"lead white",0.43}}
work(handle,{hand="body",tool="filbert 6",pile=jRestoreHalf,coverage=2.4,angle=1.36,length={12,37},edge="firm",fill=true,clip=true,seed=222})
hb=brush("filbert",4)
hb:reload(handleShadow,0.71)
hb:stroke({{475,292},{507,297},{527,327},{531,364},{505,405}},{pressure={0.62,0.11},ramps={0.13,0.29},clip=handle})
hb:reload(jRestoreLit,0.65)
hb:stroke({{450,276},{502,279},{539,315},{545,367},{512,417}},{pressure={0.67,0.13},ramps={0.13,0.35},clip=handle})
print("S2C: correct reflected light, functional handle rim and depth")

--@ chunk 12
-- Cast shadows and spare detail: connect painted objects to the stone shelf.
contact=pile{{"raw umber",2.4},{"bone black",0.38},{"yellow ochre",0.3},{"lead white",0.67}}
lightContact=pile{{"raw umber",1.3},{"yellow ochre",0.40},{"lead white",1.53},{"bone black",0.18}}
local shelf=ledge-(jug+lemons):grow(2)
work(ellipse(377,601,154,18):soften(16)*shelf,{hand="scumble",tool="filbert 8",pile=contact,coverage=1.3,angle=0.03,length={18,58},clip=shelf,seed=230})
work(ellipse(629,664,96,19):soften(14)*shelf,{hand="scumble",tool="filbert 7",pile=contact,coverage=1.35,angle=0.05,length={15,48},clip=shelf,seed=231})
work(ellipse(771,610,94,17):soften(13)*shelf,{hand="scumble",tool="filbert 7",pile=lightContact,coverage=1.2,angle=0.05,length={14,43},clip=shelf,seed=232})
-- Short aged iron knife; planar blade and its wooden handle make a new material.
blade=poly({{658,680},{703,678},{842,711},{849,727},{721,700}},true)
grip=ribbon({{833,715},{880,731},{931,746}}, {20,20,22})
steel=pile{{"lead white",1.8},{"bone black",0.44},{"raw umber",0.38},{"smalt",0.24}}
wood=pile{{"raw umber",2.8},{"bone black",0.52},{"red earth",0.45}}
work(blade,{hand="body",tool="filbert 5",pile=steel,coverage=2.0,angle=0.14,length={13,34},clip=true,fill=true,seed=233})
work(grip,{hand="body",tool="filbert 7",pile=wood,coverage=1.8,angle=0.25,length={15,35},clip=true,fill=true,seed=234})
small=brush("filbert",2.5)
small:reload(jLightAccent,0.6)
small:stroke({{697,675},{745,687},{814,705},{846,714}},{pressure={0.41,0.12},ramps={0.07,0.28},clip=blade})
-- Don't overdecorate. Fresh rust + lemon highpoint as a few deliberate touches.
tip=brush("filbert",3)
tip:reload(lemonSun,0.56)
tip:stroke({{582,565},{607,559},{637,561}},{pressure={0.52,0.10},ramps={0.15,0.34},clip=lem1})
tip:reload(lemonSun,0.56)
tip:stroke({{727,535},{746,528},{769,532}},{pressure={0.50,0.12},ramps={0.11,0.30},clip=lem2})
print("S2C: shadows contact shelf, knife and minimal finish; wait for visual quality gate")
