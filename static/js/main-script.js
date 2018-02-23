/*----------------------------------------------
    Initial Functions 
------------------------------------------------*/

  $(document).ready(function(){

/*--------- Compare Table function ---------*/
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
/*--------- ScrollingEffects Options ---------*/

    var options = {
        animationSpeed : 900,
        autoHash: false,
        headerHash: false
      };
      $.scrollingeffect(options);

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
  Line height of the arrows
--------------------------------------------------*/

  $(document).ready(setInterval(function(){
      var cardHeight = $('.owl-item.active').height();
      $('.owl-next, .owl-prev').css('line-height', cardHeight+'px');
  },
  100));

/*---------------------------------------------------
  Anchors Animations/Scrolling
--------------------------------------------------*/

  $(document).ready(function(){

   /* Tıklandığında smooth şekilde bir yere scroll etmek için*/
    $('a[href^="#"]').on('click',function(e){
          e.preventDefault();

          var target = this.hash;
          var $target = $(target);
          //scroll
           $('html, body').animate({
            /*TEHLIKE!!! NAVBAR SORUN CIKARDIGI ICIN -79 PIXEL YUKARIYA SCROLL ETMESINI SAGLADIM. ILERDE UYUMLULUK SORUNLARI CIKABILIR*/
            'scrollTop': $target.offset().top-79
           },1000, 'swing');

    });
    /*--------------------------------

    /*BACK TO THE TOP JQUERY*/
    var btt = $('back-to-top');
    btt.on('click', function(e){
        $('html, body').animate({
            scrollTop: 0
        }, 1000);

        e.preventDefault();
    });

    $(window).on('scroll', function() {

        var self = $(this),
            height = self.height();
            top = self.scrollTop();
         console.log(height);
         console.log(top);

        if (top > height)
            if (!btt.is(':visible')) {
                btt.show();
            }
            else {
                btt.hide();
            }
    });
    /*-----------------------------------------------*/
});


 