/*-------------- Animations----------------*/

// Repeat demo content
  var $body = $('body');
  var $box = $('.box');
  for (var i = 0; i < 20; i++) {
    $box.clone().appendTo($body);
  }

  // Helper function for add element box list in WOW
  WOW.prototype.addBox = function(element) {
    this.boxes.push(element);
  };

  // Init WOW.js and get instance
  var wow = new WOW();
  wow.init();

  // Attach scrollSpy to .wow elements for detect view exit events,
  // then reset elements and add again for animation
  $('.wow').on('scrollSpy:exit', function() {
    $(this).css({
      'visibility': 'hidden',
      'animation-name': 'none'
    }).removeClass('animated');
    wow.addBox(this);
  }).scrollSpy();

/*------------------------------- ------------------
    Parallax 
----------------------------------------------------*/

(function parallax()
  {

     
      function parallax1()
        {
            var parallax = document.querySelectorAll(".parallax-1"),
            speed = 0.8;

            [].slice.call(parallax).forEach(function(i)
            {

              var windowYOffset = window.pageYOffset,
                  iBackgrounPos = "center " + (0 + windowYOffset * speed) + "px";

              i.style.backgroundPosition = iBackgrounPos;

          });
        };

      function parallax2()
        {
            var parallax2 = document.querySelectorAll(".parallax-2"),
            speed = 0.5;

            [].slice.call(parallax2).forEach(function(i)
            {

              var windowYOffset = window.pageYOffset,
                  iBackgrounPos = "center " + (1350 + windowYOffset * speed) + "px";

              i.style.backgroundPosition = iBackgrounPos;

          });
        };

     window.onscroll = function() {
      parallax1();
      parallax2();
     }

  })();

/*--------------------------------------------------
Auto Image Change on Hover 
--------------------------------------------------*/

var myInterval;  // Declare it on global scope.

$('img.img-loop')
    .mouseover(function() {
    $(this).data('old-src', $(this).attr('src'));
    var alt_src = $(this).data('alt-src').split(';');

    var that = $(this);
    var i=0;
    myInterval = setInterval(function(){  // Set an interval
        if(i==alt_src.length){
            i=0;
            that.attr("src", that.data('old-src'));
        }else{
            that.attr('src', alt_src[i]);
            i++;
        }
    },500);  // Interval delay in millisecs.
})
    .mouseout(function() {
    clearInterval(myInterval);  // Clear the interval
    $(this).attr('src', $(this).data('old-src'));
});


/*----------------------------------------------
    Owl Carousel Call
------------------------------------------------*/

  $(document).ready(function(){
  $(".owl-carousel").owlCarousel();
});


/*---------------------------------------------------
    Our Services Slider
  --------------------------------------------------*/

$('.work-slider').owlCarousel({
    loop: true,
    margin:1,
    items: 5,
    dots: false,
    nav: true,
    navContainer: '#control-2',
    navText: ['<span class="lnr lnr-chevron-left"></span>','<span class="lnr lnr-chevron-right"></span>'],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1024:{
            items:5
        }
    }
})

$('.card-slider').owlCarousel({
    loop: true,
    margin:1,
    items: 1,
    dots: false,
    nav: true,
    mouseDrag: false,
    navContainer: '#control-1',
    navText: ['<i class="fa fa-chevron-left" aria-hidden="true"></i>','<i class="fa fa-chevron-right" aria-hidden="true"></i>'],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1024:{
            items:1
        }
    }
})

/*---------------------------------------------------
   Test Scripts
  --------------------------------------------------*/

  $(document).ready(function(){
      var options = {
        animationSpeed : 900
      };
      $.smartscroll(options);
  });
 