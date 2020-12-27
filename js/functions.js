AWS.config.update({
    accessKeyId: "", 
    secretAccessKey: "", 
    region: "us-east-1", 
})


function upLoadPhoto(){
    let file = document.getElementById('inputFile').files[0];
    let file_name = file.name;
    let file_type = file.type;
    let reader = new FileReader();

    var s3 = new AWS.S3();
    var params = {
        Bucket: 'album-photo-storage',
        Key: file_name,
        Body: file
    };
    s3.putObject(params, function (err, res) {
        if (err) {
            console.log("Error uploading data: ", err);
        } else {
            console.log("Successfully uploaded image to S3");
        }
    });

    reader.onload = function() {
        let arrayBuffer = this.result;
        let blob = new Blob([new Int8Array(arrayBuffer)], {
            type: file_type
        });
        let blobUrl = URL.createObjectURL(blob);

        $("#addPic").attr('src', blobUrl);
        $("#addContain").removeClass('hide');
        document.getElementById('addName').innerText = "file '" +file_name + "' uploaded!";
        console.log(blob);
    };
    reader.readAsArrayBuffer(file);
}


function diaplayItem(src, file_name) {
    let $template = $(
       ` <div class="card col-md-4">
            <img class="card-img-top" src=${src}>
            <p class="card-text">${file_name}</p>
        </div>
        <br>`
    );
    $('#picContain').append($template);
    if ($('#albumContain').hasClass('hide')) {
        $('#albumContain').removeClass('hide');
    }
}


var apigClient = apigClientFactory.newClient();
function searchPhoto() {
    $('#albumContain').addClass('hide');
    $('#addContain').addClass('hide');
    $('#picContain').empty();

    let value_input = $('#searchValue');
    let search_sentence = value_input.val();
    console.log("input: ", search_sentence);

    let params ={
        q: search_sentence,
    };
    apigClient.searchGet(params, {}, {}).then((res)=>{
        let body = res['data'];
        console.log('text: ', res)

        if(JSON.stringify(body) === '{}'){
            alert(`No match found.`)
        }
        for(let key in body) {
            let img_src = body[key];
            let img_name = key;
            diaplayItem(img_src, img_name);
        }
    }).catch((e)=>{
        console.log('Unexpected error.');
    })
}
