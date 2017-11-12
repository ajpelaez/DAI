
$("#restaurants-form").submit(function(event) {
    /* stop form from submitting normally */
    event.preventDefault();
    var $form = $( this ),
    url = $form.attr( 'action' );
    cocina = $("#cocina").find(":selected").text();
    barrio = $("#barrio").find(":selected").text();
    //$("#restaurants-box").after("<tr><td>"+barrio+"</td><td>"+barrio+"</td><td>xxxx</td></tr>");

    $.ajax({
      type: "GET",
      url: "/get-restaurants/"+cocina+"/"+barrio+"",
      success: function(result)
      {
        $("#current_restaurants").val(10);
        $("#restaurants-box").empty();
        for (var i in result)
        {
          $("#restaurants-box").append("<tr><td>"+result[i].name+"</td><td>"+result[i].address+"</td><td>"+result[i].grade+"</td></tr>");
        }
      }
    });
  });


  $("#load_more").click(function() {
    cocina = $("#cocina").find(":selected").text();
    barrio = $("#barrio").find(":selected").text();
    var numero_restaurantes = parseInt($("#current_restaurants").val());
    $("#current_restaurants").val(numero_restaurantes+10);

    $.ajax({
      type: "GET",
      url: "/get-restaurants/"+cocina+"/"+barrio+"/"+numero_restaurantes+"",
      success: function(result)
      {
        for (var i in result)
        {
          $("#restaurants-box").append("<tr><td>"+result[i].name+"</td><td>"+result[i].address+"</td><td>"+result[i].grade+"</td></tr>");
        }
      }
    });

  });
