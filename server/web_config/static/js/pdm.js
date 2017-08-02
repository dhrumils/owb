/**
* file     gateway.js
*          provides backend functions for pdm page
* author   Glide Technology Pvt. Ltd. <www.glidemtech.com>
* version  1.0
* date     29, Jul, 2017
*/

/*******************************************************************************
* constants
*******************************************************************************/

//none

/*******************************************************************************
* global variables
*******************************************************************************/

//none

/*******************************************************************************
* helper methods
*******************************************************************************/

function getAllPDMFiles(){
    $.getJSON("/pdm_get_all_files" , onGetFilesSuccess , onGetFilesFailed);
    document.getElementById("txtPDMFile").value = " ";
}

function addPDMTableRow(filelist) {
    var table = document.getElementById("tblPDMFiles");
    var rowCount = table.rows.length;

    //loop for table refresh
    for(var i = rowCount - 1 ; i >= 1 ; i--) {
        table.deleteRow(i);
    }

    rowCount = table.rows.length;

    var element;

    for (i=0; i<filelist['files'].length; i++){
        var row = table.insertRow(rowCount+i);
        row.id =  rowCount + i;
        //  alert("row" + row.id);
        var cellNum=0
        var cell = row.insertCell(cellNum);

        element = document.createElement('input');
        element.setAttribute('type','radio');
        element.id="radioButton_"+(rowCount + i);
        element.name = "Radio"
        element.innerHTML = "";
        if (filelist['files'][i]['latest'] == '1') {
            element.checked= true;
        }
        //alert(element.id);
        element.setAttribute('onclick','onPDMRadioClicked()');
        cell.appendChild(element);
        cell.align = "center";
        cellNum++;

        cell = row.insertCell(cellNum);
        element = document.createElement("span");
        //element.contentEditable= true;
        element.id="spnFilename_"+(rowCount + i);
        element.innerHTML = filelist['files'][i]['filename'];
        cell.appendChild(element);
        cell.align = "left";
        cellNum++;

        cell = row.insertCell(cellNum);
        element = document.createElement("span");
        element.id="spnModifiedDate_"+(rowCount + i);
        element.innerHTML = filelist['files'][i]['modified_date'];
        cell.appendChild(element);
        cell.align = "left";
        cellNum++;

        cell = row.insertCell(cellNum);
        element = document.createElement("span");
        element.id="spnRemarks_"+(rowCount + i);
        element.innerHTML = filelist['files'][i]['remarks'];
        cell.appendChild(element);
        cell.align = "center";
        cellNum++;

        cell = row.insertCell(cellNum);
        element = document.createElement("span");
        element.id="spnVersion_"+(rowCount + i);
        element.innerHTML = filelist['files'][i]['major_version']+'.'+filelist['files'][i]['minor_version'];
        cell.appendChild(element);
        cell.align = "left";
        cellNum++;

        cell = row.insertCell(cellNum);
        element = document.createElement("span");
        element.id= "spnAction_"+i;
        var editIcon ="<button id='btnEdit_"+(i)+"' onclick='onEditClicked(this.id)'class='glyphicon glyphicon-pencil glyphs-pdm-position'></button>";
        var deleteIcon = "<button id='btnDelete_"+(i)+"' onclick='onDeleteClicked(this.id)' class='glyphicon glyphicon-trash glyphs-pdm-position'></button>";
        var downloadIcon = "<button id='btnDownload_"+(i)+"' onclick='onDownloadClicked(this.id)' class='glyphicon glyphicon-download-alt glyphs-pdm-position'></button>"
        element.innerHTML = "";
        cell.appendChild(element);
        $("#spnAction_"+i).append(editIcon + deleteIcon + downloadIcon);
        cell.align = "left";
        cellNum++;

        if (filelist['files'][i]['latest'] == '1') {
            document.getElementById("btnDelete_"+i).disabled= true;
        }
    }
}

function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection != "undefined"
    && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}

/*******************************************************************************
* event methods
*******************************************************************************/

function onLoad(){
    getUsername();
    getAllPDMFiles();
}

$(function() {
    // We can attach the `fileselect` event to all file inputs on the page
    $(document).on('change', ':file', function() {
        var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [numFiles, label]);
    });

    // We can watch for our custom `fileselect` event like this
    $(document).ready( function() {
        $(':file').on('fileselect', function(event, numFiles, label) {

            var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

            if( input.length ) {
                input.val(log);
            } else {
                if( log ) alert(log);
            }

        });
    });

});

function onUploadFileClicked() {
    var text= $("#txtPDMFile").val();
    var formData = new FormData();
    formData.append('filePDM', $('#filePDM')[0].files[0]);

    $.ajax({
        url : '/pdm_upload_file',
        type : 'POST',
        data : formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function(data) {
            console.log(data);
            if(data['result'] == true) {
                alert("File uploaded successfully");
                getAllPDMFiles();
            } else {
                alert("Could not upload the file!");
            }
        }
    });
}

function onEditClicked(e){
    var id = e.split("_");
    row = parseInt(id[1])+1;
    document.getElementById("spnRemarks_"+row).focus();
    document.getElementById("spnRemarks_"+row).contentEditable = true;
    document.getElementById("spnRemarks_"+row).focus();
    placeCaretAtEnd( document.getElementById("spnRemarks_"+row));
    $("#spnRemarks_"+row).on('keypress', function(event) {
        if (event.keyCode == 13) {
            document.getElementById("spnRemarks_"+row).contentEditable = false;
            onSaveRemarks(row);
        }
    });
}

function onSaveRemarks() {
    var filename = document.getElementById("spnFilename_"+row).innerHTML;
    var remarks=document.getElementById("spnRemarks_"+row).innerHTML;
    var data = {'filename':filename, 'remarks':remarks};
    $.getJSON("/pdm_save_remarks", data, onSaveRemarksSuccess, onSaveRemarksFailed);
}

function onDeleteClicked(e){
    var id = e.split("_");
    row = parseInt(id[1])+1;              // a=row id, e=rowid -1//// e= button id
    var fileName=document.getElementById("spnFilename_"+row).innerHTML;
    var data = {'filename':fileName.toString()};
    $.getJSON("/pdm_delete_file", data, onDeleteSuccess, onDeleteFailed);
}

function onDownloadClicked(e){
    var id = e.split("_");
    row = parseInt(id[1])+1;
    var file =document.getElementById("spnFilename_"+row).innerHTML;
    window.open("../upload/pdm/"+file);
}

function onPDMRadioClicked(){
    document.getElementById("btnSave").disabled = false;
    document.getElementById("btnCancel").disabled = false;

}
function onCancelClicked(){
    getAllPDMFiles();
}
function onSaveClicked(){
    var table = document.getElementById("tblPDMFiles");
    var rowCount = table.rows.length;
    var filename;
    for(i=1;i<=rowCount;i++) {
        if (document.getElementById("radioButton_"+i).checked == true) {
            filename=document.getElementById("spnFilename_"+i).innerHTML;
            break;
        }
    }
    if (filename){
        var data = {'filename':filename};
        $.getJSON("/pdm_save_latest", data, onSaveLatestSuccess, onSaveLatestFailed);
        document.getElementById("btnSave").disabled = true;
    }
}

/*******************************************************************************
* success callbacks
*******************************************************************************/

function onGetFilesSuccess(filelist){
    addPDMTableRow(filelist);
}

function onSaveRemarksSuccess(data) {
    if (data['result'] == true) {
        getAllPDMFiles();
    } else {
        alert("Couldn't save remarks!");
    }
}

function onDeleteSuccess(data) {
    if (data['result'] == true) {
        getAllPDMFiles();
    } else {
        alert("Couldn't delete file!");
    }
}

function onSaveLatestSuccess(data){
    if (data['result'] = false) {
        alert ("Couldn't save the settings!");
    }
    getAllPDMFiles();
}

/*******************************************************************************
* error callbacks
*******************************************************************************/

function onGetFilesFailed(data){
    alert("Couldn't get Files!");
}

function onSaveRemarksFailed(){
    alert("Couldn't save remarks!");
    getAllPDMFiles();
}

function onDeleteFailed(){
    alert("Couldn't delete file!");
    getAllPDMFiles();
}

function onSaveLatestFailed(){
    alert ("Couldn't save the settings!");
    getAllPDMFiles();
}
