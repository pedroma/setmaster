'use strict';

angular.module('setmaster', ['ngResource'])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'partials/main.html',
        controller: 'MainCtrl'
      })
      .when('/catalog', {
        templateUrl: 'partials/catalog.html',
        controller: 'CatalogCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
