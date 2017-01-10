window.onload = (function() {
  var target = document.getElementById('result-block');
  if (target) {
    var ids = JSON.parse(target.getAttribute('data-tweet-ids'));

    for (id of ids) {
      let container = document.createElement('div');
      let input = document.createElement('input');
      container.classList.add('select-tweet-container');

      input.type = 'checkbox';
      input.value = id;
      input.name = 'select-tweet-checkbox';
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
