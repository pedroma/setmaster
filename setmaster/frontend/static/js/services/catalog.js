'use strict';

angular.module('setmaster')
  .factory('catalog', function ($resource) {
    
    var catalog = $resource("/api/catalogs/:id/:card_id",{},{'create': {method:"CREATE"}});

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
      },
      addItem: function(options, callback) {
        var add_item = new catalog(options);
        add_item.$create(options, callback);
      }
    };
  });
