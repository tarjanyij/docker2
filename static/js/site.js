// Minimal site JS referenced by base.html
document.addEventListener('DOMContentLoaded', ()=>{
  // simple helper for showing toast messages
  window.site = {
    toast(msg, timeout=3000){
      const el = document.createElement('div');
      el.textContent = msg; el.style.position='fixed'; el.style.right='18px'; el.style.bottom='18px'; el.style.background='#111'; el.style.color='#fff'; el.style.padding='8px 12px'; el.style.borderRadius='8px'; el.style.zIndex=9999; document.body.appendChild(el);
      setTimeout(()=>el.remove(), timeout);
    }
  };
  console.debug('site.js loaded');
});
