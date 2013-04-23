'use strict';

angular.module('setmaster')
  .directive('draggable', function () {
    return {
      restrict: 'A',
      link: function (scope, iElement, iAttrs, controller) {
          iElement.draggable({
              cursor: "crosshair",
              opacity: 0.35,
              helper: "clone",
              revert: true
          });
      }
    };
  });
