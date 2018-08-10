jQuery(function($){
   $("<span class='fa fa-search fise-search-icon' />").insertAfter('.LSBox .searchField');
   if (window.innerWidth < 768) {
      $(".frontpage_promo").insertBefore('.frontpage-content');
   }
   $("#edit-bar").appendTo('.page-container');
   $("#portal-globalnav").appendTo("#portal-globalnav-wrapper");
   $("#portal-header, #portal-footer, #portal-globalnav-wrapper").addClass('container');
   $("#portal-columns").removeClass('row').addClass('container');
});

