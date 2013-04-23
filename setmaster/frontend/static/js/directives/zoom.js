'use strict';

angular.module('setmaster')
  .directive('zoom', function () {
    return {
        restrict: 'A',
        link: function(scope, iElement, iAttrs, controller) {
            iElement.on('hover', function() {
                $(this).animate({width: 500});
            });
            iElement.on('mouseleave', function() {
                $(this).animate({width: 200});
            });
        }
    }
});