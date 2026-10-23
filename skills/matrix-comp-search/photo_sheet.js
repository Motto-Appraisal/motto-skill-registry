
window.sheet2 = async function(rid, maxN){
  maxN = maxN||12;
  const base='https://ntrdd.mlsmatrix.com';
  const r=await fetch(base+'/Matrix/s/ToFull?recordId='+rid+'&tableId=9');
  const t=await r.text();
  const d=new DOMParser().parseFromString(t,'text/html');
  const fd=new URLSearchParams();
  d.querySelector('form').querySelectorAll('input[type=hidden]').forEach(i=>fd.append(i.name,i.value));
  fd.set('__EVENTTARGET','m_DisplayCore');
  fd.set('__EVENTARGUMENT','DisplayInternalAction|TabSwitch|98|PHOTOS');
  const h=await (await fetch(r.url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:fd.toString()})).text();
  let urls=[...new Set([...h.matchAll(/GetMedia\.ashx\?[^"'\s<>]*/g)].map(x=>x[0].replace(/&amp;/g,'&')))].filter(u=>/Size=4/.test(u));
  const n=urls.length;
  // sample: first maxN photos
  {const body=urls.slice(3);const k=Math.min(maxN,body.length);const step=body.length/k;urls=Array.from({length:k},(_,i)=>body[Math.floor(i*step)]);}
  const cols=6,w=200,hg=150,rows=Math.ceil(urls.length/cols);
  const c=document.createElement('canvas'); c.width=cols*w; c.height=Math.max(1,rows)*hg;
  const x=c.getContext('2d'); x.fillStyle='#000'; x.fillRect(0,0,c.width,c.height);
  await Promise.all(urls.map(async(u,i)=>{try{const b=await (await fetch(base+'/mediaserver/'+u)).blob(); if(!b.size) return; const im=await createImageBitmap(b); x.drawImage(im,(i%cols)*w,Math.floor(i/cols)*hg,w,hg); x.fillStyle='#ff0'; x.font='bold 14px sans-serif'; x.fillText(String(i+1),(i%cols)*w+3,Math.floor(i/cols)*hg+14);}catch(e){}}));
  return {n,img:c.toDataURL('image/jpeg',0.55)};
};
window.batch2 = async function(list){const out={};await Promise.all(list.map(async([m,rid])=>{try{out[m]=await sheet2(rid,12)}catch(e){out[m]={err:String(e)}}}));return JSON.stringify(out)};
