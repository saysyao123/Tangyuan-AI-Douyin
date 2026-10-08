// GPT-native production stills / original Huashu renderer. Production art only for 4 validated shots.
window.MV_STYLE='gpt';
window.PUNCH=0;
window.FILM_DURATION=10.360907; // Sum of available four shots; NOT a full MV.
window.FONT_FACES=[
  {family:'NotoSansSC-500',url:'lib/fonts/NotoSansSC-500.woff'},
  {family:'LXGWWenKai-500',url:'lib/fonts/LXGWWenKai-500.woff'}
];
window.SCENE_LIBS=['scenes/gpt_images.js'];
window.ERAS=[
  {id:'l01',dur:2.5,assets:['assets/gpt/L01_clean.png']},
  {id:'l04',dur:2.75,assets:['assets/gpt/L04_hero.png'],transition:{type:'cut',dur:0.02,punch:0}},
  {id:'l07',dur:2.5,assets:['assets/gpt/L07_clean.png','assets/gpt/L07_photo.png'],transition:{type:'cut',dur:0.02,punch:0}},
  {id:'l08',dur:2.610907,assets:['assets/gpt/L08_hero.png'],transition:{type:'cut',dur:0.02,punch:0}}
];
