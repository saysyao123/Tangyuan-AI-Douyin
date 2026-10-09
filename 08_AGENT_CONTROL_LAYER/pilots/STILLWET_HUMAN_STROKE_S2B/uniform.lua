-- S2B A: mechanical uniform coverage, NOT a model of human intention
--@ chunk 2
work(cup,{hand="body",tool="filbert 9",pile=white,coverage=3.0,angle=1.55,length={17,48},fill=true,clip=true,seed=201})
work(handle,{hand="body",tool="filbert 7",pile=white,coverage=3.2,angle=1.52,length={17,36},fill=true,clip=true,seed=202})
work(cup*rect(630,510,80,420):soften(35),{hand="body",tool="filbert 6",pile=cool,coverage=2.0,angle=1.55,fill=true,clip=true,seed=203})
work(lemon+lemonTip,{hand="body",tool="filbert 9",pile=yellow,coverage=3.1,angle=0.05,length={14,42},fill=true,clip=true,seed=204})
work(lemon*ellipse(370,995,106,65):soften(20),{hand="body",tool="filbert 5",pile=darklemon,coverage=1.7,angle=0.05,length={10,28},clip=true,seed=205})
work(lemon*ellipse(265,928,100,55):soften(20),{hand="body",tool="filbert 5",pile=sun,coverage=1.7,angle=0.05,length={10,26},clip=true,seed=206})
work(rimInside,{hand="body",tool="filbert 4",pile=cool,coverage=3.0,angle=0,fill=true,clip=true,seed=207})
work(rimOuter-rimInside,{hand="detail",tool="filbert 3",pile=warmwhite,coverage=4.0,angle=0,fill=true,clip=true,seed=208})
print("S2B A: only uniform area fill, minimal intentional brush paths")
