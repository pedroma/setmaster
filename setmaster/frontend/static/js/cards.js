angular.module("Cards", ["ngResource"]);

function CardCtrl($scope, $resource) {
    $scope.cards_rsc = $resource("/api/cards/:query");
    $scope.cards = $scope.cards_rsc.get({query:undefined});

    $scope.doSearch = function() {
        $scope.cards = $scope.cards_rsc.get({query:$scope.search});
    };
}

function CatalogCtrl($scope, $resource) {
    $scope.catalog_rsc = $resource("/api/catalogs/");
    $scope.catalogs = $scope.catalog_rsc.get();
}