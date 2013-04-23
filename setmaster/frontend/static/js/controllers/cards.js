'use strict';

angular.module('setmaster')
  .controller('CatalogCtrl', function($scope, $resource, $http, cards, catalog) {
    $scope.cards = cards.get();

    $scope.doSearch = function() {
        $scope.cards = cards.get($scope.search);
    };

    $scope.catalogs = catalog.get();

    $scope.addCatalog = function() {
        catalog.create_catalog(
            {name:$scope.catalog_name},
            function () {
                $scope.catalogs = catalog.get();
                $scope.catalog_name = "";
            }
        );
    };

    $scope.deleteCatalog = function(id) {
        catalog.delete({id:id}, function() {
            $scope.catalogs = catalog.get();
        });
    };

    $scope.addToCatalog = function(event, ui) {
        var draggable = ui.draggable;
        
    }
});
