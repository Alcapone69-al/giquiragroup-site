(function(){
"use strict";
var $=function(i){return document.getElementById(i)};
var RM=window.matchMedia?matchMedia('(prefers-reduced-motion:reduce)').matches:false;
var NUM='258844266127';

/* ---- fotografias em falta: mostra a moldura em vez de um ícone partido ---- */
[].forEach.call(document.querySelectorAll('.ph img'),function(im){
  function miss(){im.parentNode.classList.add('miss')}
  if(im.complete&&im.naturalWidth===0&&im.getAttribute('src'))miss();
  im.addEventListener('error',miss);
});

[].forEach.call(document.querySelectorAll('.wm img'),function(im){im.addEventListener('error',function(){im.style.display='none'});if(im.complete&&im.naturalWidth===0)im.style.display='none'});

/* ---- ticker ---- */
var P=['Mobiliário','Eletrodomésticos','Equipamento de TI','Peças auto','Peças industriais','Acessórios de tecnologia','Material de escritório','Equipamento de hotelaria'];
var Q=['Fábrica','Inspeção','Embarque','Alfândega','Entrega','China','Moçambique'];
function fillT(el,a){if(!el)return;var h='',k,j;for(k=0;k<2;k++)for(j=0;j<a.length;j++)h+='<span>'+a[j]+'</span><i>&bull;</i>';el.innerHTML=h}
fillT($('t1'),P);fillT($('t2'),Q);

/* ---- cartão de seguimento (assinatura do herói) ---- */
var tr=$('track');
if(tr){
  var li=[].slice.call(tr.querySelectorAll('li')),pg=$('prog'),stt=$('trst'),k=0;
  var S=['Em sourcing','Em negociação','Em produção','Inspecionado','Em trânsito','Entregue'];
  function step(){
    li.forEach(function(l,i){l.className=i<k?'done':(i===k?'now':'')});
    if(pg)pg.style.transform='scaleX('+(k/(li.length-1))+')';
    if(stt)stt.textContent=S[Math.min(k,S.length-1)];
  }
  if(RM){k=li.length-1;step()}
  else{var t=0;step();setInterval(function(){t=(t+1)%(li.length+2);k=Math.min(t,li.length-1);step()},1400)}
}

/* ---- transição entre páginas ---- */
var wipe=$('wipe'),wt1;
function resetWipe(){if(!wipe)return;wipe.className='wipe nt';void wipe.offsetWidth;wipe.className='wipe'}
try{sessionStorage.removeItem('wp')}catch(e){}
if(document.documentElement.className==='wp'&&wipe){
  wipe.className='wipe in nt';document.documentElement.className='';void wipe.offsetWidth;wipe.className='wipe out';
  setTimeout(resetWipe,900);
}
window.addEventListener('pageshow',function(e){if(e.persisted){document.documentElement.className='';resetWipe()}});
document.addEventListener('click',function(e){
  if(e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  var el=e.target;while(el&&el.tagName!=='A')el=el.parentNode;
  if(!el||el.target||!el.href||el.origin!==location.origin)return;
  var clean=function(p){return p.replace(/index\.html$/,'').replace(/\.html$/,'').replace(/\/$/,'')};
  if(clean(el.pathname)===clean(location.pathname))return;
  if(RM||!wipe)return;
  e.preventDefault();
  var href=el.href;
  try{sessionStorage.setItem('wp','1')}catch(x){}
  clearTimeout(wt1);wipe.className='wipe in';
  wt1=setTimeout(function(){location.href=href},420);
});

/* ---- scroll: barra de progresso e passos ---- */
var bar=$('bar'),fl=$('fill'),stp=$('steps');
var sts=[].slice.call(document.querySelectorAll('.st'));
function sc(){
  if(bar){var d=document.documentElement,m=d.scrollHeight-window.innerHeight;
    bar.style.transform='scaleX('+(m>0?Math.min(1,Math.max(0,window.pageYOffset/m)):0)+')'}
  if(stp&&fl){
    var r=stp.getBoundingClientRect();
    var p=r.height>0?Math.min(1,Math.max(0,(window.innerHeight*0.6-r.top)/r.height)):0;
    fl.style.transform='scaleY('+p+')';
    sts.forEach(function(s){s.classList.toggle('on',s.getBoundingClientRect().top<window.innerHeight*0.62)});
  }
}
window.addEventListener('scroll',sc,{passive:true});
window.addEventListener('resize',sc);

/* ---- pedido de cotação ---- */
var fm=$('fm');
if(fm){
  var mode='lista',img=null,ref=Math.floor(1000+Math.random()*9000);
  var lk=$('lk'),ds=$('ds'),qt=$('qt'),nm=$('nm'),em=$('em'),wp=$('wp'),er=$('er'),send=$('send'),pic=$('pic'),pd=$('pd'),rd=$('rd'),tags=$('tags'),dz=$('dz'),dt=$('dt');
  $('ref').textContent=String(ref);
  var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
  var host=function(u){u=String(u||'').trim();if(!u)return '';try{return new URL(/^https?:\/\//i.test(u)?u:'https://'+u).hostname.replace(/^www\./,'')}catch(e){return ''}};
  var LBL={lista:'Descreva o que precisa',link:'O que precisa? Cor, tamanho, modelo',foto:'O que precisa? Cor, tamanho, modelo'};
  var PH={lista:'Ex.: 200 cadeiras de escritório ergonómicas, pretas, com braços. Entrega em Maputo até março.',link:'Ex.: 50 unidades, cor preta',foto:'Ex.: 50 unidades, cor preta'};
  function msg(){
    var l=['Olá Giquira Group! Gostaria de pedir uma cotação.','Ref.: GQ-'+ref];
    if(mode==='link'&&lk.value.trim())l.push('Link: '+lk.value.trim());
    if(mode==='foto')l.push('Vou anexar a foto do produto nesta conversa.');
    l.push('Pedido: '+(ds.value.trim()||'-'));
    l.push('Quantidade: '+(qt.value||'-'));
    if(dt.value)l.push('Prazo desejado: '+dt.options[dt.selectedIndex].text);
    if(nm.value.trim())l.push('Nome / empresa: '+nm.value.trim());
    if(em.value.trim())l.push('Email: '+em.value.trim());
    if(wp.value.trim())l.push('Contacto: '+wp.value.trim());
    return l.join('\n');
  }
  function relink(){send.href='https://wa.me/'+NUM+'?text='+encodeURIComponent(msg())}
  function pv(){
    var t='',q=parseInt(qt.value,10);
    if(mode==='link'){var h=host(lk.value);if(h){t+='<span class="tag">'+esc(h)+'</span>';pic.textContent='Produto em '+h}else pic.textContent='O link aparece aqui'}
    else if(mode==='foto'){if(img){pic.innerHTML='<img alt="Foto do produto escolhida" src="'+img+'">';t+='<span class="tag">Foto</span>'}else pic.textContent='A foto aparece aqui'}
    else{var lines=ds.value.trim().split(/\n+/).filter(Boolean);pic.textContent=lines.length?lines.slice(0,4).join('\n'):'A sua lista aparece aqui';if(lines.length)t+='<span class="tag">'+lines.length+(lines.length>1?' itens':' item')+'</span>'}
    if(q>0)t+='<span class="tag">'+q+' un.</span>';
    if(dt.value)t+='<span class="tag">'+esc(dt.options[dt.selectedIndex].text)+'</span>';
    tags.innerHTML=t;
    pd.textContent=(nm.value.trim()?nm.value.trim()+' · ':'')+(mode==='lista'?'Pedido por lista':(ds.value.trim()||'Comece a escrever e veja o pedido a ganhar forma.'));
    rd.hidden=true;relink();
  }
  [].forEach.call(document.querySelectorAll('.tabs button'),function(b){
    b.addEventListener('click',function(){
      mode=b.getAttribute('data-t');
      [].forEach.call(document.querySelectorAll('.tabs button'),function(x){x.setAttribute('aria-pressed',String(x===b))});
      $('bl').hidden=mode!=='link';$('bf').hidden=mode!=='foto';
      $('dsl').textContent=LBL[mode];ds.placeholder=PH[mode];ds.rows=mode==='lista'?5:3;
      pv();
    });
  });
  ['lk','ds','qt','nm','em','wp','dt'].forEach(function(i){var e=$(i);if(e){e.addEventListener('input',pv);e.addEventListener('change',pv)}});
  $('ph').addEventListener('change',function(e){
    var f=e.target.files&&e.target.files[0];if(!f)return;
    if(img)try{URL.revokeObjectURL(img)}catch(x){}
    img=URL.createObjectURL(f);dz.textContent='Trocar foto ('+f.name+')';pv();
  });
  send.addEventListener('click',function(e){
    var m='';
    if(mode==='link'&&!host(lk.value))m='Cole o link do produto ou escolha outra opção.';
    else if(mode==='foto'&&!img)m='Escolha uma foto do produto.';
    else if(!ds.value.trim())m=mode==='lista'?'Escreva o que precisa de comprar.':'Descreva o que precisa: cor, tamanho ou modelo.';
    else if(wp.value.replace(/\D/g,'').length<7)m='Indique o seu WhatsApp ou telefone para podermos responder.';
    er.textContent=m;
    if(m){e.preventDefault();return}
    relink();rd.hidden=false;
  });
  fm.addEventListener('submit',function(e){e.preventDefault()});
  pv();
}

/* ---- contactos ---- */
var cn=$('cn'),cm=$('cm'),cwa=$('cwa');
function clink(){var t='Olá Giquira Group! '+(cn.value.trim()?'Sou '+cn.value.trim()+'. ':'')+(cm.value.trim()||'Gostaria de falar com a vossa equipa.');cwa.href='https://wa.me/'+NUM+'?text='+encodeURIComponent(t)}
if(cn){cn.addEventListener('input',clink);cm.addEventListener('input',clink);clink();$('cf').addEventListener('submit',function(e){e.preventDefault()})}

/* ---- ano no rodapé ---- */
[].forEach.call(document.querySelectorAll('[data-year]'),function(e){e.textContent=new Date().getFullYear()});

sc();
})();
