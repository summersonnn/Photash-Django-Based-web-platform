/*-------------- Animations----------------*/

// Repeat demo content
  var $body = $('body');
  var $box = $('.box');
  for (var i = 0; i < 20; i++) {
    $box.clone().appendTo($body);
  }

