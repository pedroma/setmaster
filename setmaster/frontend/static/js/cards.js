var App = angular.module("Cards", ["ngResource", 'ngDragDrop']).config(function($httpProvider) {
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $httpProvider.defaults.headers.post["X-CSRFToken"]  = token;
    $httpProvider.defaults.headers.common["X-CSRFToken"]  = token;
});

App.controller("CatalogCtrl", function($scope, $resource, $http) {
    $scope.catalog_drop = [{}];
    $scope.cards_rsc = $resource("/api/cards/:query");
    $scope.cards = $scope.cards_rsc.get({query:undefined});

    $scope.doSearch = function() {
        $scope.cards = $scope.cards_rsc.get({query:$scope.search});
    };

    $scope.Catalog = $resource("/api/catalogs/:id");
    $scope.catalogs = $scope.Catalog.get({id:undefined}); // get all

    $scope.addCatalog = function() {
        var catalog = new $scope.Catalog({name:$scope.catalog_name});
        catalog.$save(function () {
            $scope.catalogs = $scope.Catalog.get();
            $scope.catalog_name = "";
        });
    };

    $scope.deleteCatalog = function(id) {
        console.log(id);
        var catalog = new $scope.Catalog({id:id});
        catalog.$delete({id:id}, function () {
            $scope.catalogs = $scope.Catalog.get();
        });
    };

    $scope.startCallback = function(event, ui) {
      console.log('You started draggin');
    };

    $scope.stopCallback = function(event, ui) {
      console.log('Why did you stop draggin me?');
    };

    $scope.dragCallback = function(event, ui) {
      console.log('hey, look I`m flying');
    };

    $scope.dropCallback = function(event, ui) {
      console.log('hey, you dumped me :-(');
        console.log($scope.catalog_drop);
    };

    $scope.overCallback = function(event, ui) {
      console.log('Look, I`m over you');
    };

    $scope.outCallback = function(event, ui) {
      console.log('I`m not, hehe');
    };
});