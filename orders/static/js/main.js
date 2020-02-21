
function optionChange(optionID){
    $("div[target]").attr("hidden", true);
    if($(`#${optionID}`).is(':checked')){
        $(`div[target="${optionID}"]`).attr("hidden", false);
    }else{
        $(`div[target="${optionID}"]`).attr("hidden", true);
    }
}
function openOrderDetail(orderID){
    $(`[name=${orderID}]`).attr("hidden", false);
    $(`#${orderID}`).attr("hidden", true);
}

function hideOrderDetail(orderID){
    $(`[name=${orderID}]`).attr("hidden", true);
    $(`#${orderID}`).attr("hidden", false);
}