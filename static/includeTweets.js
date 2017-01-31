'use strict';

let currentPage = 0;


function prevPage() {
    goToPage(currentPage - 1);
}

function nextPage() {
    goToPage(currentPage + 1);
}

function goToPage(page) {
    let target = $('.result-block');
    if (target) {
        let numPages = $('.page-container').length;
        currentPage = Math.max(0, Math.min(page, numPages - 1));

        // Show page container
        $('.page-container').hide();
        $('.page-container.page-' + currentPage).show();

        // Update pagination controls
        $('.page-num-span').text(currentPage + 1);
        if(currentPage == 0) {
            $('.page-nav.prev').css('visibility', 'hidden');
        }
        else {
            $('.page-nav.prev').css('visibility', 'visible');
        }
        if(currentPage == numPages - 1) {
            $('.page-nav.next').css('visibility', 'hidden');
        }
        else {
            $('.page-nav.next').css('visibility', 'visible');
        }
    }
}

$(document).ready(function() {
    // Navigate to first page
    goToPage(0);

    // Insert tweet widgets
    $('.tweet').each(function(t, tweet) {
        twttr.widgets.createTweet(
            $(this).attr('id'),
            tweet,
            {
                theme: 'dark',
                width: '500px',
                align: 'center'
            }
        );
    });
});
