angular.module("Cards", ["ngResource"]).config(function($httpProvider) {
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $httpProvider.defaults.headers.post["X-CSRFToken"]  = token;
    $httpProvider.defaults.headers.common["X-CSRFToken"]  = token;
});

function CardCtrl($scope, $resource) {
    $scope.cards_rsc = $resource("/api/cards/:query");
    $scope.cards = $scope.cards_rsc.get({query:undefined});

    $scope.doSearch = function() {
        $scope.cards = $scope.cards_rsc.get({query:$scope.search});
    };
}

function CatalogCtrl($scope, $resource, $http) {
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
}