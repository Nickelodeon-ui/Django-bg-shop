$(document).ready(function () {
    var LowerBorder = 9
    var a = document.getElementById("items__inner")

    $(".more").click(function () {
        $.ajax({
            type: 'GET',
            url: `./more-bg/${LowerBorder}`,
            success: function (response) {
                const boardgames = response.data
                if (boardgames.length != 0) {
                    console.log(a.innerHTML) //Доделать показать больше
                    console.log("done")
                } else {
                    // Вернуло пустой массив нужно убрать кнопку показать еще
                    console.log("No")
                }
            }
        });
    });
});