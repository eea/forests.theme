jQuery(function($){
   $("<span class='fa fa-search fise-search-icon' />").insertAfter('.searchField');
   if (window.innerWidth < 768) {
      $(".frontpage_promo").insertBefore('.frontpage-content');
   }
});
