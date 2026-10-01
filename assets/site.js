/* Giquira Group — comportamento do site (sem dependências).
   Índice: 1 utilitários · 2 transição entre páginas · 3 cabeçalho, progresso e passos · 4 menu móvel
           5 entradas ao scroll · 6 cartão de seguimento · 7 vídeos · 8 pedido de cotação · 9 contactos · 10 botão WhatsApp */
(function(){
"use strict";
var $=function(i){return document.getElementById(i)};
var $$=function(s,c){return [].slice.call((c||document).querySelectorAll(s))};
var RM=window.matchMedia?matchMedia('(prefers-reduced-motion:reduce)').matches:false;
var root=document.documentElement;
var NUM=(document.body.getAttribute('data-wa')||'258844266127');
function store(k,v){try{if(v===undefined)return sessionStorage.getItem(k);if(v===null)sessionStorage.removeItem(k);else sessionStorage.setItem(k,v)}catch(e){return null}}

/* ── 2 transição entre páginas ───────────────────────────────────────────── */
var wipe=$('wipe'),wd=$('wd'),leaving=false,LABELS={};
try{LABELS=JSON.parse(wipe&&wipe.getAttribute('data-labels')||'{}')}catch(e){}
function pageKey(p){p=p.split('/').pop()||'index.html';return p.indexOf('.html')<0?p+'.html':p}
function arrive(){
  if(!wipe)return;
  if(root.classList.contains('wp')){
    if(wd)wd.textContent=store('wpl')||'';
    wipe.classList.add('out');
    setTimeout(function(){root.classList.remove('wp');wipe.classList.remove('out')},1000);
  }
  store('wp',null);store('wpl',null);
}
arrive();
window.addEventListener('pageshow',function(e){
  if(e.persisted&&wipe){leaving=false;root.classList.remove('wp');wipe.className='wipe'}
});
document.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  var a=e.target.closest&&e.target.closest('a');
  if(!a||a.target||a.hasAttribute('download')||!a.href||a.origin!==location.origin)return;
  var samePage=pageKey(a.pathname)===pageKey(location.pathname);
  if(samePage)return; /* âncoras na mesma página seguem o normal */
  if(RM||!wipe||leaving)return;
  e.preventDefault();leaving=true;
  var label=LABELS[pageKey(a.pathname)]||'';
  if(wd)wd.textContent=label;
  store('wp','1');store('wpl',label);
  closeMenu(true);
  wipe.classList.remove('out');void wipe.offsetWidth;wipe.classList.add('in');
  setTimeout(function(){location.href=a.href},620);
});

/* ── 3 cabeçalho, barra de progresso e passos ────────────────────────────── */
var hdr=document.querySelector('header'),bar=$('bar'),fl=$('fill'),stp=$('steps'),sts=$$('.st'),ticking=false;
function onScroll(){
  var y=window.pageYOffset,d=root.scrollHeight-window.innerHeight;
  if(hdr)hdr.classList.toggle('scrolled',y>8);
  if(bar)bar.style.transform='scaleX('+(d>0?Math.min(1,Math.max(0,y/d)):0)+')';
  if(stp&&fl){
    var r=stp.getBoundingClientRect(),vh=window.innerHeight;
    var p=r.height>0?Math.min(1,Math.max(0,(vh*0.6-r.top)/r.height)):0;
    fl.style.transform='scaleY('+p+')';
    sts.forEach(function(s){s.classList.toggle('on',s.getBoundingClientRect().top<vh*0.62)});
  }
  ticking=false;
}
function req(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}}
window.addEventListener('scroll',req,{passive:true});
window.addEventListener('resize',req);
onScroll();

/* ── 4 menu móvel ────────────────────────────────────────────────────────── */
var tog=$('mtog'),panel=$('mpanel'),lastFocus=null;
function openMenu(){
  if(!panel)return;lastFocus=document.activeElement;
  panel.classList.add('open');panel.removeAttribute('inert');tog.setAttribute('aria-expanded','true');tog.setAttribute('aria-label','Fechar menu');
  root.classList.add('lock');
  var f=panel.querySelector('a');if(f)setTimeout(function(){f.focus({preventScroll:true})},200);
}
function closeMenu(silent){
  if(!panel||!panel.classList.contains('open'))return;
  panel.classList.remove('open');panel.setAttribute('inert','');tog.setAttribute('aria-expanded','false');tog.setAttribute('aria-label','Abrir menu');
  root.classList.remove('lock');
  if(!silent&&lastFocus)lastFocus.focus({preventScroll:true});
}
if(tog&&panel){
  panel.setAttribute('inert','');
  tog.addEventListener('click',function(){panel.classList.contains('open')?closeMenu():openMenu()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu()});
  panel.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&a.hash&&pageKey(a.pathname)===pageKey(location.pathname))closeMenu(true)});
  window.addEventListener('resize',function(){if(window.innerWidth>960)closeMenu(true)});
}

/* ── 5 entradas ao scroll ────────────────────────────────────────────────── */
var rv=$$('[data-rv],[data-img]');
if(RM||!('IntersectionObserver' in window)){rv.forEach(function(el){el.classList.add('in')})}
else{
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}});
  },{rootMargin:'0px 0px -8% 0px',threshold:0.12});
  rv.forEach(function(el){io.observe(el)});
}

/* ── 6 cartão de seguimento (assinatura do herói) ────────────────────────── */
var tr=$('track');
if(tr){
  var li=$$('li',tr),pg=$('prog'),stt=$('trst'),k=0,t=0,tid=null;
  var S=['Em sourcing','Em negociação','Em produção','Inspecionado','Em trânsito','Entregue'];
  var step=function(){
    li.forEach(function(l,i){l.className=i<k?'done':(i===k?'now':'')});
    if(pg)pg.style.transform='scaleX('+(k/(li.length-1))+')';
    if(stt)stt.textContent=S[Math.min(k,S.length-1)];
  };
  if(RM){k=li.length-1;step()}
  else{
    step();
    var run=function(){if(tid)return;tid=setInterval(function(){t=(t+1)%(li.length+2);k=Math.min(t,li.length-1);step()},1400)};
    var stop=function(){clearInterval(tid);tid=null};
    /* só anima quando está visível, para poupar bateria */
    if('IntersectionObserver' in window){new IntersectionObserver(function(es){es[0].isIntersecting?run():stop()}).observe(tr)}else run();
    document.addEventListener('visibilitychange',function(){document.hidden?stop():run()});
  }
}

/* ── 7 vídeos: botão de reprodução próprio; só um vídeo a tocar de cada vez ─ */
var vids=$$('.vid');
vids.forEach(function(f){
  var v=f.querySelector('video'),b=f.querySelector('.play');if(!v||!b)return;
  b.addEventListener('click',function(){
    vids.forEach(function(o){var ov=o.querySelector('video');if(ov&&ov!==v&&!ov.paused)ov.pause()});
    v.controls=true;f.classList.add('playing');
    var p=v.play();if(p&&p.catch)p.catch(function(){});
  });
  v.addEventListener('ended',function(){f.classList.remove('playing');v.controls=false;v.load()});
});

/* ── 8 pedido de cotação ─────────────────────────────────────────────────── */
var fm=$('fm');
if(fm){
  var mode='lista',img=null,ref=Math.floor(1000+Math.random()*9000);
  var lk=$('lk'),ds=$('ds'),qt=$('qt'),nm=$('nm'),em=$('em'),wp=$('wp'),er=$('er'),send=$('send'),pic=$('pic'),pd=$('pd'),rd=$('rd'),tags=$('tags'),dz=$('dz'),dt=$('dt'),ind=document.querySelector('.tabs .ind');
  $('ref').textContent=String(ref);
  var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
  var host=function(u){u=String(u||'').trim();if(!u)return '';try{return new URL(/^https?:\/\//i.test(u)?u:'https://'+u).hostname.replace(/^www\./,'')}catch(e){return ''}};
  var LBL={lista:'Descreva o que precisa',link:'O que precisa? Cor, tamanho, modelo',foto:'O que precisa? Cor, tamanho, modelo'};
  var PH={lista:'Ex.: 200 cadeiras de escritório ergonómicas, pretas, com braços. Entrega em Maputo até março.',link:'Ex.: 50 unidades, cor preta',foto:'Ex.: 50 unidades, cor preta'};
  var msg=function(){
    var l=['Olá Giquira Group! Gostaria de pedir uma cotação.','Ref.: GQ-'+ref];
    if(mode==='link'&&lk.value.trim())l.push('Link: '+lk.value.trim());
    if(mode==='foto')l.push('Vou anexar a foto do produto nesta conversa.');
    l.push('Pedido: '+(ds.value.trim()||'-'));
    if(qt.value)l.push('Quantidade: '+qt.value);
    if(dt.value)l.push('Prazo desejado: '+dt.options[dt.selectedIndex].text);
    if(nm.value.trim())l.push('Nome / empresa: '+nm.value.trim());
    if(em.value.trim())l.push('Email: '+em.value.trim());
    if(wp.value.trim())l.push('Contacto: '+wp.value.trim());
    return l.join('\n');
  };
  var relink=function(){send.href='https://wa.me/'+NUM+'?text='+encodeURIComponent(msg())};
  var pv=function(){
    var tg='',q=parseInt(qt.value,10);
    if(mode==='link'){var h=host(lk.value);if(h){tg+='<span class="tag">'+esc(h)+'</span>';pic.textContent='Produto em '+h}else pic.textContent='O link aparece aqui'}
    else if(mode==='foto'){if(img){pic.innerHTML='<img alt="Foto do produto escolhida" src="'+img+'">';tg+='<span class="tag">Foto</span>'}else pic.textContent='A foto aparece aqui'}
    else{var lines=ds.value.trim().split(/\n+/).filter(Boolean);pic.textContent=lines.length?lines.slice(0,4).join('\n'):'A sua lista aparece aqui';if(lines.length)tg+='<span class="tag">'+lines.length+(lines.length>1?' itens':' item')+'</span>'}
    if(q>0)tg+='<span class="tag">'+q+' un.</span>';
    if(dt.value)tg+='<span class="tag">'+esc(dt.options[dt.selectedIndex].text)+'</span>';
    tags.innerHTML=tg;
    pd.textContent=(nm.value.trim()?nm.value.trim()+' · ':'')+(mode==='lista'?(ds.value.trim()?'Pedido por lista':'Comece a escrever e veja o pedido a ganhar forma.'):(ds.value.trim()||'Comece a escrever e veja o pedido a ganhar forma.'));
    rd.hidden=true;relink();
  };
  var moveInd=function(b){if(!ind||!b)return;ind.style.width=b.offsetWidth+'px';ind.style.transform='translateX('+b.offsetLeft+'px)'};
  var tabs=$$('.tabs button');
  tabs.forEach(function(b){
    b.addEventListener('click',function(){
      mode=b.getAttribute('data-t');
      tabs.forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});
      moveInd(b);
      $('bl').hidden=mode!=='link';$('bf').hidden=mode!=='foto';
      $('dsl').textContent=LBL[mode];ds.placeholder=PH[mode];ds.rows=mode==='lista'?5:3;
      er.textContent='';pv();
    });
  });
  moveInd(tabs[0]);window.addEventListener('resize',function(){moveInd(document.querySelector('.tabs button[aria-pressed=true]'))});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){moveInd(document.querySelector('.tabs button[aria-pressed=true]'))});
  ['lk','ds','qt','nm','em','wp','dt'].forEach(function(i){var x=$(i);if(x){x.addEventListener('input',function(){x.removeAttribute('aria-invalid');pv()});x.addEventListener('change',pv)}});
  $('ph').addEventListener('change',function(e){
    var f=e.target.files&&e.target.files[0];if(!f)return;
    if(img)try{URL.revokeObjectURL(img)}catch(x){}
    img=URL.createObjectURL(f);dz.textContent='Trocar foto ('+f.name+')';pv();
  });
  send.addEventListener('click',function(e){
    var m='',bad=null;
    if(mode==='link'&&!host(lk.value)){m='Cole o link do produto ou escolha outra opção.';bad=lk}
    else if(mode==='foto'&&!img){m='Escolha uma foto do produto.';bad=$('ph')}
    else if(!ds.value.trim()){m=mode==='lista'?'Escreva o que precisa de comprar.':'Descreva o que precisa: cor, tamanho ou modelo.';bad=ds}
    else if(wp.value.replace(/\D/g,'').length<7){m='Indique o seu WhatsApp ou telefone para podermos responder.';bad=wp}
    else if(em.value.trim()&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value.trim())){m='O email não parece completo.';bad=em}
    er.textContent=m;
    if(m){e.preventDefault();if(bad){bad.setAttribute('aria-invalid','true');if(bad.focus&&bad.type!=='file')bad.focus()}return}
    relink();rd.hidden=false;
  });
  fm.addEventListener('submit',function(e){e.preventDefault()});
  pv();
}

/* ── 9 contactos ─────────────────────────────────────────────────────────── */
var cn=$('cn'),cm=$('cm'),cwa=$('cwa');
if(cn&&cm&&cwa){
  var clink=function(){var t='Olá Giquira Group! '+(cn.value.trim()?'Sou '+cn.value.trim()+'. ':'')+(cm.value.trim()||'Gostaria de falar com a vossa equipa.');cwa.href='https://wa.me/'+NUM+'?text='+encodeURIComponent(t)};
  cn.addEventListener('input',clink);cm.addEventListener('input',clink);clink();
  $('cf').addEventListener('submit',function(e){e.preventDefault()});
}

/* ── 10 botão de WhatsApp: esconde-se no rodapé e junto aos formulários ──── */
var fab=document.querySelector('.fab');
if(fab&&'IntersectionObserver' in window){
  var hide=new Set();
  var fo=new IntersectionObserver(function(es){
    es.forEach(function(en){en.isIntersecting?hide.add(en.target):hide.delete(en.target)});
    fab.classList.toggle('away',hide.size>0);
  },{threshold:0.05});
  $$('footer,#pedido,#cf').forEach(function(el){fo.observe(el)});
}

$$('[data-year]').forEach(function(e){e.textContent=new Date().getFullYear()});
})();
