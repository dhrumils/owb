/**
* file     settings.js
*          provides backend functions for general settings page
* author   Glide Technology Pvt. Ltd. <www.glidemtech.com>
* version  1.0
* date     31, Jul, 2017
*/

/*******************************************************************************
* constants
*******************************************************************************/

/*******************************************************************************
* global variables
*******************************************************************************/

/*******************************************************************************
* helper methods
*******************************************************************************/

/*******************************************************************************
* event methods
*******************************************************************************/
function onLoad(){
    getUsername();
    getMemoryUsageGateway();
    getMemoryUsagePDM();
}

function getMemoryUsageGateway(){
    $.getJSON("/get_memory_usage_gateway",onGetMemoryUsageGatewaySuccess,onGetMemoryUsageGatewayFail);
}

function getMemoryUsagePDM(){
    $.getJSON("/get_memory_usage_pdm",onGetMemoryUsagePDmSuccess,onGetMemoryUsagePDmFail);
}

/*******************************************************************************
* Success callbacks
*******************************************************************************/

function onGetMemoryUsageGatewaySuccess(memory_usage_gateway){
    document.getElementById("lblGatewayMemory").innerHTML= memory_usage_gateway +" " + "bytes";
}

function onGetMemoryUsagePDmSuccess(memory_usage_pdm){
    document.getElementById("lblPDMMemory").innerHTML= memory_usage_pdm +" " + "bytes";
}
/*******************************************************************************
* Error callbacks
*******************************************************************************/

function onGetMemoryUsageGatewayFail(){
    alert("Failed to get Memory Usage of Gateway");
}

function onGetMemoryUsagePDmFail(){
    alert("Failed to get Memory Usage of PDM");
}


/*******************************************************************************
* End of File
*******************************************************************************/
