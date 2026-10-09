-- S2B B: semantic-first, body-following painter choreography.
-- Every stroke is physically executed by Stillwet. No paste, no target-image renderer.
--@ chunk 2
-- Establish a recognizable cup before spending time on small texture.
work(handle,{hand="body",tool="filbert 11",pile=cool,coverage=1.4,angle=function(x,y) return 1.3 + (x-750)/950 end,
 length={20,54},angle_jitter=0.14,load=0.55,clip=true,seed=211})
work(cup,{hand="body",tool="filbert 14",pile=white,coverage=1.9,
 angle=function(x,y) return 1.57 + 0.20*math.sin((x-591)/85) end,
 length={24,72},angle_jitter=0.13,curve={0.08,0.07},load=0.62,dips={3,0.72,0.88},fill=true,clip=true,seed=212})
-- Model an actual turning cylinder, not a texture covering a cylinder.
work(cup*rect(626,506,100,415):soften(40),{hand="body",tool="filbert 9",pile=cool,coverage=1.25,angle=1.57,length={24,69},load=0.40,clip=true,seed=213})
work(cup*rect(482,519,122,345):soften(48),{hand="body",tool="filbert 10",pile=warmwhite,coverage=1.15,angle=1.53,length={29,67},load=0.40,clip=true,seed=214})

-- The viewer should first see an actual CUP; lip and handle gestures are intentional arcs.
b=brush("filbert",5)
b:reload(warmwhite,0.70)
b:stroke({{484,507},{535,526},{594,533},{658,524},{705,507}},{pressure={0.70,0.12},ramps={0.09,0.32},clip=cup+rimOuter})
b:reload(cool,0.42)
b:stroke({{490,488},{542,467},{594,463},{646,472},{700,492}},{pressure={0.55,0.12},ramps={0.08,0.40},clip=rimOuter})
work(rimInside,{hand="body",tool="filbert 5",pile=cool,coverage=2.4,angle=0,length={15,32},clip=true,seed=215})
b=brush("filbert",7)
b:reload(warmwhite,0.75)
b:stroke({{699,590},{768,567},{814,616},{832,685},{801,758},{713,784}},{pressure={0.66,0.12},ramps={0.08,0.35},clip=handle})
-- Sparse long downstrokes over highlights: vertical stroke order reads like hand movement.
b=brush("filbert",11)
b:reload(white,0.72)
for _,x in ipairs({515,550,590,615}) do
 b:stroke({{x,546},{x-6,631},{x-9,737},{x+1,855}},{pressure={0.69,0.14},ramps={0.10,0.30},clip=cup})
end

-- Lemon: topography guides the stroke, not a row of horizontal sample marks.
work(lemon+lemonTip,{hand="body",tool="filbert 12",pile=yellow,coverage=2.0,
 angle=function(x,y) return -0.23+0.72*((y-965)/130) end,
 length={18,53},angle_jitter=0.18,curve={0.22,0.12},fill=true,clip=true,seed=216})
work(lemon*ellipse(368,1003,116,57):soften(24),{hand="body",tool="filbert 8",pile=darklemon,coverage=1.05,angle=0.30,
 length={17,43},load=0.4,clip=true,seed=217})
work(lemon*ellipse(262,924,121,54):soften(25),{hand="body",tool="filbert 7",pile=sun,coverage=1.15,angle=-0.26,
 length={14,34},load=0.42,clip=true,seed=218})
-- Intentional single-gesture contours across curved fruit.
b=brush("filbert",7)
b:reload(sun,0.72)
for _,path in ipairs({
 {{201,955},{220,937},{258,924},{301,920}},
 {{209,969},{245,953},{300,946},{354,952}},
 {{245,1006},{296,1002},{348,988},{399,969}}
}) do
 b:stroke(path,{pressure={0.64,0.10},ramps={0.10,0.32},clip=lemon})
end
-- Cloth fold occurs in the TABLE, never on the cup / fruit.
b=brush("filbert",10)
b:reload(cloth,0.35)
b:stroke({{18,1128},{200,1104},{398,1120},{598,1150},{820,1136},{981,1114}},{pressure={0.3,0.08},clip=tableTop-objs})
print("S2B B: intentional shape-following, pressure-tapered strokes on Stillwet canvas")
