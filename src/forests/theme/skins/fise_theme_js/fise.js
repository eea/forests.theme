jQuery(function($){
   if (window.innerWidth < 768) {
      $(".frontpage_promo").insertBefore('.frontpage-content');
   }
   $("#edit-bar").appendTo('.page-container');
   $("#portal-globalnav").appendTo("#portal-globalnav-wrapper");
   $("#portal-footer, #portal-globalnav-wrapper").addClass('container');
   var $portal_columns = $("#portal-columns");
   $portal_columns.removeClass('row').addClass('container');

    $('.login i').on('click', function() {
        $(this).toggleClass('action-selected');
        $('.search i').removeClass('action-selected');
        $('.login-container ').animate({
            'height': 'toggle'
        }, 200);
        $('#portal-searchbox ').animate({
            'height': 'hide'
        }, 200);
    });

    $('.search i').on('click', function() {
        $(this).toggleClass('action-selected');
        $('.login i').removeClass('action-selected');
        $('#portal-searchbox ').animate({
            'height': 'toggle'
        }, 200);
        $('.login-container ').animate({
            'height': 'hide'
        }, 200);
    });
});
