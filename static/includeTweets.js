window.onload = (function(){
  var target = document.getElementById('result-block');
  if(target) {
    var ids = JSON.parse(target.getAttribute('data-tweet-ids'));

    for(id of ids) {
      twttr.widgets.createTweet(
      id.toString(), target,
      {
        theme: 'dark',
        width: '500px',
        align: 'center'
      }
      );
    }
  }
});
