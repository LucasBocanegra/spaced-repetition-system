/**
 * Created by lucas on 27/06/16.
 */
$(function () {
    var translate = $(".translate");
    var question = $("#answer");

    $(translate).hide();
    $(question).hide();

    $('#view').on("click",function () {
        $(translate).show();
        $(question).show(500);
        $(this).hide();

    });
    
    
});