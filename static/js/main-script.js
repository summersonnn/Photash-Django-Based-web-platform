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
});


/*---------------------------------------------------
    Photopool Item Slider Options
  --------------------------------------------------*/

$('.photopool-slider').owlCarousel({
    loop: false,
    items: 1,
    dots: false,
    nav: true,
    mouseDrag: false,
    navContainer: '#photopool-control-1',
    navText: ['<i class="fa fa-caret-left" aria-hidden="true"></i>','<i class="fa fa-caret-right" aria-hidden="true"></i>']
});



/*---------------------------------------------------
  Line height of the arrows
--------------------------------------------------*/

if($('.photopool-main-wrapper')) {   // Execute only if Photopool Slider Present on Page !

  $(document).ready(setInterval(function(){
      var cardHeight = $('.owl-item.active>.photopool-img-wrapper').height();
      $('.owl-next, .owl-prev').css('line-height', cardHeight+'px');
  },
  100));
}

  

/*---------------------------------------------------
  Anchors Animations/Scrolling
--------------------------------------------------*/

  /*$(document).ready(function(){

    Tıklandığında smooth şekilde bir yere scroll etmek için
    $('a[href^="#"]').on('click',function(e){
          e.preventDefault();

          var target = this.hash;
          var $target = $(target);
          //scroll
           $('html, body').animate({
            /*TEHLIKE!!! NAVBAR SORUN CIKARDIGI ICIN -79 PIXEL YUKARIYA SCROLL ETMESINI SAGLADIM. ILERDE UYUMLULUK SORUNLARI CIKABILIR
            'scrollTop': $target.offset().top-79
           },1000, 'swing');

    });
    /*--------------------------------

    BACK TO THE TOP JQUERY
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
});*/



if($('.feeds-wrapper')) {         // Execute only if its the Feed Page !

   var $grid = $('.feeds-wrapper').masonry({
    itemSelector: '.feed-item',
    percentPosition: true,
    columnWidth: '.grid-sizer',
    horizontalOrder:true
  });
// layout Masonry after each image loads so there can't be any issue with padding between items when page is initially loaded
  $grid.imagesLoaded().progress( function() {
      $grid.masonry();
  });  


  $(document).ready(function(){
      var val = 1;

      $(".feed-overlay>button.btn-txt-only").click(function(){
          if (val== 1) {
              $(this).siblings('.btn-report').show();
              val = 0;
          }

          else {
              val = 1;
              $(this).siblings('.btn-report').hide();
          }

          return false;
      });

      $(".contest-detail-content-wrap #prize-open-btn").click(function(){
          if (val== 1) {
              $(this).siblings('.prize-list').show();
              val = 0;
          }

          else {
              val = 1;
              $(this).siblings('.prize-list').hide();
          }

          return false;
      });

   });

}


 




 