/* Minimal nav_sidebar.js stub for Django admin */
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    try {
      var toggle = document.getElementById('nav-sidebar-toggle');
      if (toggle) {
        toggle.addEventListener('click', function(){
          document.body.classList.toggle('collapsed-nav');
        });
      }
    } catch(e) {
      // swallow errors
      console.error('nav_sidebar.js error', e);
    }
  });
})();
