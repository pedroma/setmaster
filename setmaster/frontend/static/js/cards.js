angular.module("Cards", ["ngResource"]);

function CardCtrl($scope, $resource) {
    $scope.cards_rsc = $resource("/api/cards/:query");
    $scope.cards = $scope.cards_rsc.get({query:undefined});

    $scope.doSearch = function() {
        $scope.cards = $scope.cards_rsc.get({query:$scope.search});
    };
}