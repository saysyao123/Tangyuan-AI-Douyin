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
