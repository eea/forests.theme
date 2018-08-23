jQuery(function($){
   $("<span class='fa fa-search fise-search-icon' />").insertAfter('.LSBox .searchField');
   if (window.innerWidth < 768) {
      $(".frontpage_promo").insertBefore('.frontpage-content');
   }
   $("#edit-bar").appendTo('.page-container');
   $("#portal-globalnav").appendTo("#portal-globalnav-wrapper");
   $("#portal-header, #portal-footer, #portal-globalnav-wrapper").addClass('container');
   var $portal_columns = $("#portal-columns");
   $portal_columns.removeClass('row');
   var $left_column = $("#portal-column-one");
   var $body = $("body");
   if ($left_column.length) {
      $body.addClass('fise-two-columns');
   }
   else {
       $portal_columns.addClass('container');
   }
   $(".header-info").insertBefore("#portal-personaltools-wrapper");
   $("#navbar").insertBefore(".header-info");
});

