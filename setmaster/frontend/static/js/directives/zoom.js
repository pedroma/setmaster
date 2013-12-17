'use strict';

angular.module('setmaster')
  .directive('zoom', function () {
    return {
        restrict: 'A',
        link: function(scope, iElement, iAttrs, controller) {
            iElement.on('mouseenter', function() {
                var position = $(this).position();
                var $new_img = $(this).clone();
                $new_img.css("position", "absolute");
                $new_img.css("z-index", 99);
                $new_img.offset(position);
                $("body").prepend($new_img);
                $new_img.on("mouseleave", function() {
                    $(this).css("z-index", 1);
                    $(this).animate({width: 200, left: position.left, top:position.top}, function() {
                        $(this).remove();
                    });
                });
                $new_img.animate({width: 350, left: position.left-100, top:position.top-20});
            });
        }
    }
});