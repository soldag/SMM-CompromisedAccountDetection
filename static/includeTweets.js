'use strict';

window.onload = (function() {
  let target = document.getElementById('result-block');
  if (target) {
    let ids = JSON.parse(target.getAttribute('data-tweet-ids').replace(/'/g, '"'));
    let scores = JSON.parse(target.getAttribute('data-tweet-scores').replace(/'/g, '"'));

    if(ids.length !== scores.length) {
      console.log('ERROR! Number of Ids does not match number of scores.')
    }

    for (let i = 0; i < ids.length; i++) {
      let container = document.createElement('div');
      let input = document.createElement('input');
      let colorScale = document.createElement('div');
      container.classList.add('select-tweet-container');

      input.type = 'checkbox';
      input.value = ids[i];
      input.name = 'confident_tweet_id';
      input.classList.add('select-tweet-checkbox');

      colorScale.classList.add('circle--color-scale');
      if(scores[i] > 0 && scores[i] <= 0.5) {
        colorScale.classList.add('circle--color-scale--yellow');
      }
      if(scores[i] > 0.5 && scores[i] <= 0.85) {
        colorScale.classList.add('circle--color-scale--orange');
      }
      if(scores[i] > 0.85 && scores[i] <= 1) {
        colorScale.classList.add('circle--color-scale--red');
      }

      twttr.widgets.createTweet(
        ids[i].toString(), container, {
          theme: 'dark',
          width: '500px',
          align: 'center'
        }
      );
      target.appendChild(container);
      container.appendChild(input);
      container.appendChild(colorScale)
    }
  }
});
