'use strict';

angular.module('setmaster')
  .factory('catalog', function ($resource) {
    
    var catalog = $resource("/api/catalogs/:id");

    return {
      get: function(id) {
        return catalog.get({id:id});  
      },
      create_catalog: function(options, callback) {
        var new_cat = new catalog(options);
        new_cat.$save(callback);
      },
      delete: function(options, callback) {
        var to_delete = new catalog(options);
        to_delete.$delete(options, callback);
      }
    };
  });
