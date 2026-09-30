(() => {
 'use strict';
 const meta={'pt-BR':['Português','br'],'en-US':['English','us'],'es-ES':['Español','es'],'zh-CN':['中文','cn'],'hi-IN':['हिन्दी','in'],'ar-SA':['العربية','sa'],'fr-FR':['Français','fr'],'bn-BD':['বাংলা','bd'],'ru-RU':['Русский','ru'],'de-DE':['Deutsch','de'],'it-IT':['Italiano','it'],'ja-JP':['日本語','jp']};
 const $=id=>document.getElementById(id),button=$('languageButton'),menu=$('languageMenu');
 let language='pt-BR';try{const saved=localStorage.getItem('factorytoolbox-language');if(meta[saved])language=saved;}catch{}
 const t=key=>window.FactoryTranslations[language][key]??window.FactoryTranslations['pt-BR'][key]??key;
 for(const [code,[label,flag]]of Object.entries(meta)){
  const option=document.createElement('button');option.type='button';option.setAttribute('role','option');option.dataset.language=code;
  const image=document.createElement('img');image.src=`flags/${flag}.svg`;image.alt='';option.append(image,document.createTextNode(label));menu.append(option);
  option.addEventListener('click',()=>{applyLanguage(code);setMenu(false);button.focus();});
 }
 function setMenu(open){menu.hidden=!open;button.setAttribute('aria-expanded',String(open));if(open)menu.querySelector(`[data-language="${language}"]`).focus();}
 function applyLanguage(code,persist=true){
  if(!meta[code])return;language=code;document.documentElement.lang=code;document.documentElement.dir=code==='ar-SA'?'rtl':'ltr';
  document.querySelectorAll('[data-i18n]').forEach(node=>node.textContent=t(node.dataset.i18n));
  document.title=`Factory Toolbox — ${t('headline')} ${t('accent')}`;
  document.querySelector('meta[name="description"]').content=t('intro');document.querySelector('meta[property="og:description"]').content=t('intro');
  $('currentFlag').src=`flags/${meta[code][1]}.svg`;$('currentLanguage').textContent=meta[code][0];button.setAttribute('aria-label',`${t('language')}: ${meta[code][0]}`);menu.setAttribute('aria-label',t('language'));
  menu.querySelectorAll('button').forEach(option=>option.setAttribute('aria-selected',String(option.dataset.language===code)));
  if(persist)try{localStorage.setItem('factorytoolbox-language',code);}catch{}
 }
 button.addEventListener('click',()=>setMenu(menu.hidden));
 document.addEventListener('click',event=>{if(!event.target.closest('#languagePicker'))setMenu(false);});
 $('languagePicker').addEventListener('keydown',event=>{
  if(event.key==='Escape'){setMenu(false);button.focus();event.stopPropagation();}
  if(['ArrowDown','ArrowUp','Home','End'].includes(event.key)){event.preventDefault();if(menu.hidden){setMenu(true);return;}const options=[...menu.children],index=options.indexOf(document.activeElement),next=event.key==='Home'?0:event.key==='End'?options.length-1:(index+(event.key==='ArrowDown'?1:-1)+options.length)%options.length;options[next].focus();}
 });
 // These tools share the GitHub Pages origin. Carry the explicitly selected language
 // through their existing preference keys without sending anything over the network.
 document.querySelectorAll('.tool-card').forEach(card=>card.addEventListener('click',()=>{try{localStorage.setItem(card.dataset.storage,language);}catch{}}));
 applyLanguage(language,false);
})();
