$(document).ready(function($) {
    $('.cidades').change(function(){
        var url = "get_bairro/"
        url = url + document.form.cidades.value;
        console.log(url)
        $.ajax({
            url: url,
//            url: "get_bairro/1",
            type: "GET",
//            data: $(this).serialize(),

            success: function(json) {
//                console.log(json)
                for(j=document.form.bairro.options.length-1;j>=0;j--) {
                    document.form.bairro.remove(j);
                }

                for(i = 0; i < json.length; i++){
                    var optn = document.createElement("OPTION");
                    optn.text = json[i].nome;
                    optn.value = json[i].id;
                    document.form.bairro.options.add(optn);
                }
            }
        })
    })
})