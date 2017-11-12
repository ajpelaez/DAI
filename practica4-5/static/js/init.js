(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.modal').modal();

    $(document).ready(function() {
        $('select').material_select();
      });

    $('#change_style').click(function(){
      $("nav").toggleClass( "light-blue accent-3" );
      $("footer").toggleClass("light-blue accent-3");
    });


  }); // end of document ready
})(jQuery); // end of jQuery name space
