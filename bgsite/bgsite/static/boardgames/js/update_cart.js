$(document).ready(function () {

    $(".update_btn").prop('disabled', true);

    $(".qty_btn").click(function(){
        $(".update_btn").prop('disabled', false);
    });

    $(".update_btn").click(function () {
        var data = {}
        var titles = $('span[class=title]');
        var qtys = $('input[class=number]');
        var length = titles.length //У этих массивов будет все равно одинаковое количество так как у каждой игры будет количество
        
        for (let i = 0; i < length; i++) {
            data[titles[i].innerText] = qtys[i].value; 
        }

        data['csrfmiddlewaretoken'] = getCookie('csrftoken');

        $.ajax ({
              type: 'POST',
              url: './cart/update-cart',
              data: data,
              success: function(response){
                if (response.status == 1) {
                    // Сообщение пользователю?  
                    window.location = response.url;
                } else {
                    alert(response.message);
                }
              }
            });
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}