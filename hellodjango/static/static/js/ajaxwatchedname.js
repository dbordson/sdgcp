// This code watches the watchlist star (ticker dashboard
// page) and when it sees a click, it goes to the 
// watchtoggle view in sdapp/views.py and then it
// saves the new state of the watchlist watchstoggle.html
// which is dynamically rendered into the dashboard / screens view
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