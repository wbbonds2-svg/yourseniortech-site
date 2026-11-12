/* Senior Tech Foundation: text size control (Normal, Large, Larger). Remembers the choice on this device. */
(function(){
  var KEY='stf-text-size', sizes=[100,115,130], names=['Normal','Large','Larger'], i=0;
  try{ var s=parseInt(localStorage.getItem(KEY),10); if(sizes.indexOf(s)>-1) i=sizes.indexOf(s); }catch(e){}
  function apply(){ document.documentElement.style.fontSize=sizes[i]+'%'; }
  apply();
  function build(){
    var bar=document.querySelector('.topbar .wrap'); if(!bar||document.getElementById('text-size')) return;
    var st=document.createElement('style');
    st.textContent='#text-size{display:inline-flex;align-items:center;gap:8px;white-space:nowrap;margin:4px 0}'+
      '#text-size .ts-btn{min-width:44px;height:44px;padding:0 8px;border:2px solid #fff;border-radius:8px;background:transparent;color:#fff;font-family:inherit;font-weight:800;line-height:1;cursor:pointer}'+
      '#text-size .ts-0{font-size:16px}#text-size .ts-1{font-size:21px}#text-size .ts-2{font-size:26px}'+
      '#text-size .ts-btn[aria-pressed="true"]{background:#fff;color:#10263a}'+
      '#text-size .ts-btn:focus-visible{outline:3px solid #ffc94d;outline-offset:2px}';
    document.head.appendChild(st);
    var box=document.createElement('span'); box.id='text-size'; box.setAttribute('role','group'); box.setAttribute('aria-label','Text size');
    var lab=document.createElement('span'); lab.textContent='Text size:'; box.appendChild(lab);
    sizes.forEach(function(sz,n){
      var b=document.createElement('button'); b.type='button'; b.textContent='A'; b.className='ts-btn ts-'+n;
      b.setAttribute('aria-label',names[n]+' text size'); b.setAttribute('title',names[n]); b.setAttribute('aria-pressed', n===i ? 'true' : 'false');
      b.addEventListener('click',function(){
        i=n; apply(); try{ localStorage.setItem(KEY,String(sizes[i])); }catch(e){}
        box.querySelectorAll('button').forEach(function(x,k){ x.setAttribute('aria-pressed', k===i ? 'true' : 'false'); });
      });
      box.appendChild(b);
    });
    bar.appendChild(box);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',build); else build();
})();
