$(function(){
    $('.menu-modal').hide();
    $('#list-name').on("click", function() {
      $('.menu-modal').slideToggle('slow');
    });
});
