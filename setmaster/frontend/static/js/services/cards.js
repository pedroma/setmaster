'use strict';

angular.module('setmaster')
  .service('cards', function ($resource) {
    var cards_rsc = $resource("/api/cards/:query");
    
    return {
      get: function (query) {
        return cards_rsc.get({query:query});
      }
    };
  });
