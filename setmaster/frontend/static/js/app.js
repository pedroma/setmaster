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
  }).config(function($httpProvider) {
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $httpProvider.defaults.headers.post["X-CSRFToken"]  = token;
    $httpProvider.defaults.headers.common["X-CSRFToken"]  = token;
});
