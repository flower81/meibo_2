$(function(){

  $('.btn').click(function(){
    $('.sidebar').animate({width: 'toggle'}, 'slow');
  });

  var nav    = $('.border'),
    offset = nav.offset();

    $(window).scroll(function () {
      if($(window).scrollTop() > offset.top - 75) {
        nav.addClass('fixed');
      } else {
        nav.removeClass('fixed');
      }
    });

});
