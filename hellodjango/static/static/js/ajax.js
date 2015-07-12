// This code watches the searchsubmit button (on the dashboard
// / screens page) and when it sees a click, it draws data into the 
// searchsignals view in sdapp/views.py and then it generates
// a modal with the help of ajax_search.html which is dynamically
// rendered into the dashboard / screens view
$(function(){

    $('#searchsubmit').click(function() {
        $.ajax({
            
            type: "POST",
            
            url: "/sdapp/search/",
            traditional: true,
            data: {
                'search_text' : $('#search').val(),
                'selectbox' : $('#selectbox').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            
            success: searchSuccess,
            dataType: 'html'
        });
        // document.write($('#selectbox').val());
    });
});

// $( document ).ajaxStart( function() {
//     document.write('start');
// });

// $( document ).ajaxStart( function() {
//     document.write('stop');
// });


function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);
    $('#resultsmodal').modal('show');
}