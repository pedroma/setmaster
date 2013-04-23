'use strict';

angular.module('setmaster')
  .directive('droppable', function () {
    return {
      restrict: 'A',
      link: function (scope, iElement, iAttrs, controller) {
          iElement.droppable({
                hoverClass: "drop-hover",
                tolerance: "pointer",
                drop: function(event, ui) {
                    var draggable = ui.draggable;
                }
          });
      }
    };
  });
