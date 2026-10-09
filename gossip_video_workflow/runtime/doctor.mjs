import {chromium} from 'playwright';
const b=await chromium.launch({headless:true});
try {const p=await b.newPage(); await p.setContent('<p>中文流程检查</p>'); console.log(JSON.stringify({chromium:b.version(),ready:await p.textContent('p')}));}
finally{await b.close();}
