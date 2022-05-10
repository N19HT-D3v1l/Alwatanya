$(document).ready(function() {

    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    
    var tableRows = $('#table-body tr #options').children().each(function(){
        var confirmed = $(this).data("confirmed")
        // console.log($(this).data("confirmed"))
        
        // $("#Approve").each(function(){
        //     $(this).attr("disabled", true);
        //     //do your stuff, you can use $(this) to get current cell
        // })
        // console.log(this.querySelector(".btn-outline-primary"))
        
        var approveBtn = this.querySelector(".btn-outline-primary");
        var disApproveBtn = this.querySelector(".btn-outline-danger");
        if (confirmed == "True") {
            $(approveBtn).attr("disabled", true);
            $(disApproveBtn).attr("disabled", false);
            
        }else{
            $(approveBtn).attr("disabled", false);
            $(disApproveBtn).attr("disabled", true);
        }

    });


    // .each(function(){
    //     var confirmed = $("#Approve").data("confirmed");
    //     console.log(this);
    //     // this.innerText = "Test Scam"
    // });

    // var confirmed = $("#Approve").data("confirmed");
    // console.log(confirmed);

    // if (confirmed == "True") {
    //     approveBtn.attr("disabled", true);
    //     disApproveBtn.attr("disabled", false);
        
    // }else{
    //     approveBtn.attr("disabled", false);
    //     disApproveBtn.attr("disabled", true);
    // }

    $('#table-body').on('click', '.btn-outline-primary' ,function(){
        var dataId = $(this).data('id');
        
        // console.log(this)

        $.ajax({
            url: '/dashboard/'+dataId+'/approve/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId
            },
            type: 'post',
        }).done(function (response) { 
            // console.log(response.content);
            // var at = document.getElementById('alert_ajax_success')
            // at.innerText = response.content
            


            // var abtn = $(this).querySelector("#Approve");
            // $(abtn).attr("disabled", true);
    //         $(disApproveBtn).attr("disabled", false);
            document.getElementById("Approve"+dataId).disabled = true;
            document.getElementById("Disapprove"+dataId).disabled = false;
            
            $("#alert_ajax_success").fadeTo(2000, 500).slideUp(500, function(){
                $("#alert_ajax_success").slideUp(500);
                // at.innerText = ''
            });
        })
        .fail(function (jqXHR, textStatus, errorThrown) { 

            $("#alert_ajax_error").fadeTo(2000, 500).slideUp(500, function(){
                $("#alert_ajax_error").slideUp(500);
            });
        });
    });
    $('#table-body').on('click', '.btn-outline-danger', function(){
        var dataId = $(this).data('id');
        // console.log(dataId)


        $.ajax({
            url: '/dashboard/'+dataId+'/disapprove/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId
            },
            type: 'post',
        }).done(function (response) { 
            console.log(response.content);

            document.getElementById("Approve"+dataId).disabled = false;
            document.getElementById("Disapprove"+dataId).disabled = true;

            $("#alert_ajax_success").fadeTo(2000, 500).slideUp(500, function(){
                $("#alert_ajax_success").slideUp(500);
            });
            
        })
        .fail(function (jqXHR, textStatus, errorThrown) { 

            $("#alert_ajax_error").fadeTo(2000, 500).slideUp(500, function(){
                $("#alert_ajax_error").slideUp(500);
            });
        });
    });
});
