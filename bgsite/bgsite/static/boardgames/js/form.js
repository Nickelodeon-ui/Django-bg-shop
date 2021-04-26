$(document).ready(function () {
    // For suggestion bgs form 
    $(".formstart_btn").click(function () {
        $(".hidden_form-background").show()
        $(".hidden_form-background").css("height", $(document).height());
        $(".footer__form").fadeIn(500);
        $(".hidden_form-background").addClass("selected");
        $(".footer__form").addClass("selected");
    });

    $(".hidden_form-background").click(function () {
        if ($(this).hasClass("selected")) {
            $(this).hide();
            $(".footer__form").hide();
            $(this).removeClass("selected");
            $(".footer__form").removeClass("selected");
        }
    });

    $(".footer_form-img").click(function () {
        // Exactly the same only for cross    
        if ($(".hidden_form-background").hasClass("selected")) {
            $(".hidden_form-background").hide();
            $(".footer__form").hide();
            $(".hidden_form-background").removeClass("selected");
            $(".footer__form").removeClass("selected");
        }
    })

});