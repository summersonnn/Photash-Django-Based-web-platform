
(function() {
  var root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Foxfix = (function() {
    function Foxfix(stability, sensitivity, tolerance, delay) {
      this.stability = stability != null ? Math.abs(stability) : 8;
      this.sensitivity = sensitivity != null ? 1 + Math.abs(sensitivity) : 100;
      this.tolerance = tolerance != null ? 1 + Math.abs(tolerance) : 1.1;
      this.delay = delay != null ? delay : 150;
      this.lastUpDeltas = (function() {
        var i, ref, results;
        results = [];
        for (i = 1, ref = this.stability * 2; 1 <= ref ? i <= ref : i >= ref; 1 <= ref ? i++ : i--) {
          results.push(null);
        }
        return results;
      }).call(this);
      this.lastDownDeltas = (function() {
        var i, ref, results;
        results = [];
        for (i = 1, ref = this.stability * 2; 1 <= ref ? i <= ref : i >= ref; 1 <= ref ? i++ : i--) {
          results.push(null);
        }
        return results;
      }).call(this);
      this.deltasTimestamp = (function() {
        var i, ref, results;
        results = [];
        for (i = 1, ref = this.stability * 2; 1 <= ref ? i <= ref : i >= ref; 1 <= ref ? i++ : i--) {
          results.push(null);
        }
        return results;
      }).call(this);
    }

    Foxfix.prototype.check = function(e) {
      var lastDelta;
      e = e.originalEvent || e;
      if (e.wheelDelta != null) {
        lastDelta = e.wheelDelta;
      } else if (e.deltaY != null) {
        lastDelta = e.deltaY * -40;
      } else if ((e.detail != null) || e.detail === 0) {
        lastDelta = e.detail * -40;
      }
      this.deltasTimestamp.push(Date.now());
      this.deltasTimestamp.shift();
      if (lastDelta > 0) {
        this.lastUpDeltas.push(lastDelta);
        this.lastUpDeltas.shift();
        return this.isInertia(1);
      } else {
        this.lastDownDeltas.push(lastDelta);
        this.lastDownDeltas.shift();
        return this.isInertia(-1);
      }
      return false;
    };

    Foxfix.prototype.isInertia = function(direction) {
      var lastDeltas, lastDeltasNew, lastDeltasOld, newAverage, newSum, oldAverage, oldSum;
      lastDeltas = direction === -1 ? this.lastDownDeltas : this.lastUpDeltas;
      if (lastDeltas[0] === null) {
        return direction;
      }
      if (this.deltasTimestamp[(this.stability * 2) - 2] + this.delay > Date.now() && lastDeltas[0] === lastDeltas[(this.stability * 2) - 1]) {
        return false;
      }
      lastDeltasOld = lastDeltas.slice(0, this.stability);
      lastDeltasNew = lastDeltas.slice(this.stability, this.stability * 2);
      oldSum = lastDeltasOld.reduce(function(t, s) {
        return t + s;
      });
      newSum = lastDeltasNew.reduce(function(t, s) {
        return t + s;
      });
      oldAverage = oldSum / lastDeltasOld.length;
      newAverage = newSum / lastDeltasNew.length;
      if (Math.abs(oldAverage) < Math.abs(newAverage * this.tolerance) && (this.sensitivity < Math.abs(newAverage))) {
        return direction;
      } else {
        return false;
      }
    };

    Foxfix.prototype.showLastUpDeltas = function() {
      return this.lastUpDeltas;
    };

    Foxfix.prototype.showLastDownDeltas = function() {
      return this.lastDownDeltas;
    };

    return Foxfix;

  })();

}).call(this);



(function ($) { 
  var MOUSE_EVENTS_STRING = 'mousewheel DOMMouseScroll wheel MozMousePixelScroll';

  var lethargy;
  if (typeof Lethargy !== 'undefined' && Lethargy !== null) {
    lethargy = new Lethargy();
  }

 
   // FUNCTIONS
   

  var getWindowTop = function () {
    return Math.max(
    
      window.pageYOffset,

      window.document.body.scrollTop,

      window.document.documentElement.scrollTop
    );
  };

  $.scrollingeffect = function scrollingeffect(overrides) { 
    /**
     * OPTIONS
     */
    var options = $.extend({}, $.scrollingeffect.defaults, overrides);

    // If `options.sectionSelector` is not set, use `options.sectionClass`
    if (!options.sectionSelector) {
      options.sectionSelector = '.' + options.sectionClass;
    }

    if (
      typeof EventEmitter === 'undefined'
      || EventEmitter === null
      || (options.eventEmitter && options.eventEmitter.constructor !== EventEmitter)
    ) {
      options.eventEmitter = null;
    }

    if (options.bindSwipe) {
      var xDown = null;
      var yDown = null;

      var handleTouchStart = function (event) {
        var e = event.originalEvent || event;
        xDown = e.touches[0].clientX;
        yDown = e.touches[0].clientY;
      };

      var handleTouchMove = function (event) {
        var e = event.originalEvent || event;
        if (!xDown || !yDown) {
          return;
        }

        var xUp = e.touches[0].clientX;
        var yUp = e.touches[0].clientY;

        var xDiff = xDown - xUp;
        var yDiff = yDown - yUp;

        if (Math.abs(xDiff) > Math.abs(yDiff)) {
          if (xDiff > 0) {
            options.eventEmitter.emitEvent('swipeLeft');
          } else {
            options.eventEmitter.emitEvent('swipeRight');
          }
        } else if (yDiff > 0) {
          options.eventEmitter.emitEvent('swipeUp');
        } else {
          options.eventEmitter.emitEvent('swipeDown');
        }
        /* reset values */
        xDown = null;
        yDown = null;
      };
    }

    /**
     * RUNTIME VARIABLES
     */

    // Whether jQuery is currently animating the scroll event
    var isScrolling = false;

    var sections = [];

    var sectionWrapperTop;
    var sectionWrapperBottom;

    var validBreakPoint = false;
    var belowBreakpoint = false;

    var currentHash = window.location.hash;

    // Store the current section wrapper method for later use
    var sectionWrapper = $(options.sectionWrapperSelector + ':first');

    /**
     * FUNCTIONS
     */

    // Check if the view is currently within the section wrapper
    var sectionWrapperIsVisible = function () {
      var windowTop = getWindowTop();
      var windowBottom = windowTop + $(window).height();
      // Only affect scrolling if within the sectionWrapper area
      if (
        windowBottom > sectionWrapperTop
        && windowTop <= sectionWrapperBottom
      ) {
        return true;
      }
      return false;
    };

    // Update the values for `sections`
    var calculateSectionBottoms = function () {
      var tmpSections = [];
      sectionWrapperTop = Math.round(
        sectionWrapper.position().top
        + parseInt(sectionWrapper.css('paddingTop'), 10)
        + parseInt(sectionWrapper.css('borderTopWidth'), 10)
        + parseInt(sectionWrapper.css('marginTop'), 10));

      // We use `height()` instead of `innerHeight()` or `outerHeight()`
      // because we don't care about the padding in the sectionWrapper at the bottom
      sectionWrapperBottom = Math.round(
        sectionWrapperTop
        + sectionWrapper.height(), 10);
      tmpSections.push(sectionWrapperTop);
      $(options.sectionSelector).each(function (i, el) {
        tmpSections.push(Math.round(
          sectionWrapperTop
          + $(el).position().top // This will be relative to the sectionWrapper
          + $(el).outerHeight()
        ));
      });
      sections = tmpSections;
    };

    var getScrollAction = function (e) {
      var validScroll;
      if (lethargy) {
        validScroll = lethargy.check(e);
      }
      // Do nothing if it is already scrolling
      if (!isScrolling) {
        if (lethargy) {
          if (validScroll === 1) {
            return 'up';
          } else if (validScroll === -1) {
            return 'down';
          }
        } else if (e.originalEvent.wheelDelta > 0 || e.originalEvent.detail < 0) {
          return 'up';
        } else if (e.originalEvent.wheelDelta < 0 || e.originalEvent.detail > 0) {
          return 'down';
        }
      }
      return false;
    };

    var getSectionIndexAt = function (position) {
      for (var i = 0; i < sections.length; i += 1) {
        if (position <= sections[i]) {
          return i;
        }
      }
      return sections.length;
    };

    var autoHash = function () {
      var newHash;
      if ((getWindowTop() + ($(window).height() / 2)) < sectionWrapperTop) {
        newHash = options.headerHash;
      } else {
        var slideIndex = getSectionIndexAt(getWindowTop() + ($(window).height() / 2));
        if (slideIndex !== undefined) {
          newHash = $(options.sectionSelector + ':nth-of-type(' + (slideIndex + 1) + ')').data('hash');
        }
      }
      if (typeof newHash === 'undefined' || !(window.location.hash === ('#' + newHash))) {
        if (typeof newHash === 'undefined') {
          newHash = options.headerHash;
        }
        if (!options.keepHistory) {
          window.location.replace(window.location.href.split('#')[0] + '#' + newHash);
        } else {
          window.location.hash = newHash;
        }
      }
    };

    var scrollToPixel = function (pixel, speed) {
      if (isScrolling) {
        return;
      }
      isScrolling = true;
      $('body,html').stop(true, true).animate({
        scrollTop: pixel,
      }, speed, function () { 
        isScrolling = false;
        if (options.eventEmitter) {
          options.eventEmitter.emitEvent('scrollEnd');
        }
      });
    };

    // Make this public
    this.scroll = function scroll(down) {
      if (sections) {
        var windowTop = getWindowTop();
        if (options.eventEmitter) {
          var sectionIndexAtWindowMiddle = getSectionIndexAt(windowTop + ($(window).height() / 2));
          var nextSlideNumber = down ? (
            sectionIndexAtWindowMiddle + 1
          ) : (
              sectionIndexAtWindowMiddle - 1
          );
          options.eventEmitter.emitEvent('scrollStart', [nextSlideNumber]);
        }
        for (var i = 0; i < sections.length; i += 1) {
          if (windowTop < sections[i]) {
            if (down) {
              scrollToPixel(sections[i], 700);
            } else {
              scrollToPixel(sections[i - 1] - $(window).height(), 700);
            }
            if (options.eventEmitter) {
              options.eventEmitter.emitEvent('scrollEnd');
            }
            return false;
          }
        }
      }
      return undefined;
    };


    // Bind scroll events and perform scrolljacking
    var bindScroll = function () {
      $(window).bind(MOUSE_EVENTS_STRING, function (e) { // eslint-disable-line func-names
        var scrollAction = getScrollAction(e);
        if (options.dynamicHeight) {
          calculateSectionBottoms();
        }
        var windowTop = getWindowTop();
        var windowBottom = windowTop + $(window).height();
        // Only affect scrolling if within the sectionWrapper area
        if (
          windowBottom > sectionWrapperTop
          && windowTop <= sectionWrapperBottom
        ) {
         
          var sectionIndexAtWindowTop = getSectionIndexAt(windowTop);
          var sectionIndexAtWindowMiddle = getSectionIndexAt(windowTop + ($(window).height() / 2));
          var sectionIndexAtWindowBottom = getSectionIndexAt(windowBottom);
          if (sectionIndexAtWindowTop !== sectionIndexAtWindowBottom
            || !options.innerSectionScroll) {
            e.preventDefault();
            e.stopPropagation();
            if (scrollAction) {
              if (scrollAction === 'up') {
                if (options.toptotop) {
                  scrollToPixel(
                    sections[sectionIndexAtWindowMiddle - 2] + 1
                    , options.animationSpeed
                  );
                } else {
                  scrollToPixel(
                    sections[sectionIndexAtWindowMiddle - 1] - $(window).height()
                    , options.animationSpeed
                  );
                }
                if (options.eventEmitter) {
                  options.eventEmitter.emitEvent('scrollStart', [sectionIndexAtWindowMiddle - 1]);
                }
              } else if (scrollAction === 'down') {
                scrollToPixel(sections[sectionIndexAtWindowMiddle] + 1, options.animationSpeed);
                if (options.eventEmitter) {
                  options.eventEmitter.emitEvent('scrollStart', [sectionIndexAtWindowMiddle + 1]);
                }
              }
            }
          }
        }
      });
    };

    // Remove all functions bound to mouse events
    var unbindScroll = function () {
      $(window).unbind(MOUSE_EVENTS_STRING);
    };

    /**
     * INITIAL SETUP
     */

    sectionWrapper.css({
      position: 'relative',
    }); 
    setTimeout(function () { 
      calculateSectionBottoms();

      // autoHash

      if (options.autoHash) {
        if (options.eventEmitter !== null && !options.hashContinuousUpdate) {
          options.eventEmitter.addListener('scrollEnd', autoHash);
        } else {
          
          $(window).bind('scroll', autoHash);
        }
      }

      if (options.initialScroll && currentHash.length > 0) {
        // Remove the '#' from the hash and use jQuery to check
        // if an element exists with that hash in the 'data-hash' attribute
        var matchedObject = $('[data-hash="' + currentHash.substr(1) + '"]');
        // If there is a matched element, scroll to the first element at time 0 (immediately)
        if (matchedObject.length > 0) {
          scrollToPixel(matchedObject[0].offsetTop + sectionWrapperTop, 0);
        }
      }
    }, 50);

    $(window).bind('resize', calculateSectionBottoms);

    if (
      options.breakpoint !== null
      && options.breakpoint === parseInt(options.breakpoint, 10)
      && options.breakpoint > 0
    ) {
      validBreakPoint = true;
    }

    if (options.mode === 'vp') {
      // IE8 does not support viewport
      if (options.ie8) {
        var resizeToVP = function () {
          $(options.sectionSelector).css({
            height: $(window).height(),
          });
        };

        resizeToVP();

        $(window).bind('resize', resizeToVP);
      } else {
        $(options.sectionSelector).css({
          height: '100vh',
        });
      }
    }

    if (options.sectionScroll) {
      if (validBreakPoint) {
      
        $(window).bind('resize', function () {
          // Unbind scroll
          if ($(window).width() < options.breakpoint) {
            // Only unbind once (minimize resource usage)
            if (!belowBreakpoint) {
              unbindScroll();
              
              belowBreakpoint = true;
              return false;
            }
          } else if (belowBreakpoint) {
            // If the screen width is currently equal to or above the breakpoint
            // Bind scroll only if it's not bound already
            bindScroll();
            belowBreakpoint = false;
          }
          return undefined;
        });
      }
      bindScroll();
    }

    if (options.bindSwipe) {
      $(window).on('touchstart', handleTouchStart); 
      $(window).on('touchmove', handleTouchMove); 
    }
    if (options.bindKeyboard) {
      var handleKeydown = function (event) {
        var e = event.originalEvent || event;
        if (options.dynamicHeight) {
          calculateSectionBottoms();
        }
        var windowTop = getWindowTop();
        var windowBottom = windowTop + $(window).height();
        if (sectionWrapperIsVisible()) {
          
          var sectionIndexAtWindowTop = getSectionIndexAt(windowTop);
          var sectionIndexAtWindowMiddle = getSectionIndexAt(windowTop + ($(window).height() / 2));
          var sectionIndexAtWindowBottom = getSectionIndexAt(windowBottom);
          if (sectionIndexAtWindowTop !== sectionIndexAtWindowBottom
            || !options.innerSectionScroll) {
            switch (e.which) {
              // up arrow
              case 38:
                e.preventDefault();
                e.stopPropagation();
                if (options.toptotop) {
                  scrollToPixel(
                    sections[sectionIndexAtWindowMiddle - 2] + 1
                    , options.animationSpeed);
                } else {
                  scrollToPixel(
                    sections[sectionIndexAtWindowMiddle - 1] - $(window).height()
                    , options.animationSpeed);
                }
                if (options.eventEmitter) {
                  options.eventEmitter.emitEvent('scrollStart', [sectionIndexAtWindowMiddle - 1]);
                }
                break;
              // down arrow
              case 40:
                e.preventDefault();
                e.stopPropagation();
                scrollToPixel(sections[sectionIndexAtWindowMiddle] + 1, options.animationSpeed);
                if (options.eventEmitter) {
                  options.eventEmitter.emitEvent('scrollStart', [sectionIndexAtWindowMiddle + 1]);
                }
                break;

              default:
            }
          }
        }
      };
      $(window).on('keydown', handleKeydown);
    }
    return this;
  };

  // Set default options
  $.scrollingeffect.defaults = { // eslint-disable-line no-param-reassign
    animationSpeed: 700,
    autoHash: true,
    breakpoint: null,
    initialScroll: true,
    headerHash: 'header',
    keepHistory: false,
    mode: 'vp', // "vp", "set"
    sectionClass: 'section',
    sectionSelector: null,
    sectionScroll: true,
    sectionWrapperSelector: '.section-wrapper',
    eventEmitter: null,
    dynamicHeight: false,
    ie8: false,
    hashContinuousUpdate: true,
    innerSectionScroll: true,
    toptotop: false,
    bindSwipe: true,
    bindKeyboard: true,
  };
}(jQuery));
