'use strict';

angular.module('setmaster')
  .controller('CatalogCtrl', function($scope, $resource, $http, cards, catalog) {
    $scope.cards = cards.get();

    $scope.doSearch = function() {
        $scope.cards = cards.get($scope.search);
    };

    $scope.catalogs = catalog.get();

    $scope.addCatalog = function() {
        var options = {name:$scope.catalog_name};
        catalog.create_catalog(options,
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
        var options = {
            card_id: ui.draggable.data("multiverseid"),
            id: $(this).data("catalogid")
        };
        catalog.addItem(options, function() {
            $scope.catalogs = catalog.get();
        });
        
    }
});
