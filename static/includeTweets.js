'use strict';

window.onload = (function() {
  let target = document.getElementById('result-block');
  if (target) {
    let ids = JSON.parse(target.getAttribute('data-tweet-ids').replace(/'/g, '"'));

    for (let id of ids) {
      let container = document.createElement('div');
      let input = document.createElement('input');
      container.classList.add('select-tweet-container');

      input.type = 'checkbox';
      input.value = id;
      input.name = 'confident_tweet_id';
      input.classList.add('select-tweet-checkbox');
      
      twttr.widgets.createTweet(
        id.toString(), container, {
          theme: 'dark',
          width: '500px',
          align: 'center'
        }
      );
      target.appendChild(container);
      container.appendChild(input);
    }
  }
});
