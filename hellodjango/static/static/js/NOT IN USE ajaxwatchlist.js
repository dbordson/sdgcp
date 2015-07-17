// NOT CURRENTLY IN USE
$('body').on('click','#watchtoggle',function() {  
    var ticker = $(this).data('ticker')
    console.log(ticker);
    var toggleSuccess = function(data, textStatus, jqXHR) {
        
        $('#watchstatus' + ticker).html(data);
    }
    $.ajax({
        
        type: "POST",
        
        url: "/sdapp/watchtoggle/",
        traditional: true,     
        data: {
            'ticker' : ticker,
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },       
        success: toggleSuccess,
        dataType: 'html'
    });

    
});

// $( document ).ajaxStart( function() {
//     document.write('start');
// });

// $( document ).ajaxStart( function() {
//     document.write('stop');
// });


// function toggleSuccess(data, textStatus, jqXHR, ticker)
// {
//     console.log(ticker);
//     $('#watchstatus').html(data);
// }