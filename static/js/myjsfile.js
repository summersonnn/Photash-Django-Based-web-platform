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

