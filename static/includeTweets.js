'use strict';

$(document).ready(function() {
    // Render tweet widgets
    $('.tweet-container').each(function() {
        let id = $(this).data('tweet-id');
        twttr.widgets.createTweet(id, this, {
            theme: 'dark',
            width: '500px',
            align: 'center'
        });
    });

    // Enable tooltips
    $('.score-indicator').tooltip({
        placement: 'left'
    });
});
