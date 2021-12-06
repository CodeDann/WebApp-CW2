function showOrder(x) {
  console.log(x)
  var order = document.getElementById(x);
  console.log(order)
  order.classList.remove("starthidden");
}

$(document).ready(function() {

    $('.close').click(function () {
        $(".alert").fadeOut("slow");
    });

    $("#displayer").click(function() {
         $("#order").show()
    });



    $('.speaker').click(function(){
      var text = $('#information').text();
      var msg = new SpeechSynthesisUtterance();
      var voices = window.speechSynthesis.getVoices();
      msg.voice = voices[0];
      msg.rate = 5;
      msg.pitch = 2;
      msg.text = text;

      speechSynthesis.speak(msg);
    });


});
