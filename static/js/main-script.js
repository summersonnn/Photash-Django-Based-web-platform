/*----------------------------------------------
    Card Slider function call
------------------------------------------------*/
/*---------------------------------------------------
   Table Script
  --------------------------------------------------*/

  $(document).ready(function(){
    $('.comp-table tr>td:first-child').hover(function(){
        $('.features-title .title-height-add').css('top', '-20px');
        $('.premium-title .title-height-add').css('top', '0px');
    },
      function(){
        $('.features-title .title-height-add').css('top', '0px');
        $('.premium-title .title-height-add').css('top', '-20px');
      }
    );

    $('.comp-table tr>td:last-child').hover(function(){
        $('.regular-title .title-height-add').css('top', '-20px');
        $('.premium-title .title-height-add').css('top', '0px');
    },
      function(){
        $('.regular-title .title-height-add').css('top', '0px');
        $('.premium-title .title-height-add').css('top', '-20px');
      }
    );

  });

  /****************************************************/

$(document).ready(function(){
  $(".owl-carousel").owlCarousel();
});




/*---------------------------------------------------
    Cards Options
  --------------------------------------------------*/

$('.card-slider').owlCarousel({
    loop: false,
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
        }
    }
});

/*---------------------------------------------------
  Options for the scrolling effect
  --------------------------------------------------*/

  $(document).ready(function(){
      var options = {
        animationSpeed : 900,
        autoHash: false,
        headerHash: false
      };
      $.scrollingeffect(options);
  });

  /*---------------------------------------------------
  Line height of the arrows
  --------------------------------------------------*/

  $(document).ready(setInterval(function(){
      var cardHeight = $('.owl-item.active').height();
      $('.owl-next, .owl-prev').css('line-height', cardHeight+'px');
  },
      100));
 