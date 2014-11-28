'use strict';

var viewsPath = static_folder + 'angular/app/views/';
var states = [];

var home = {}
home.name = 'home';
home.url = '/home';
home.templateUrl = viewsPath + 'main.html';
home.controller = 'MainCtrl';
states.push(home);

var results = {}
results.name = 'results';
results.url = '/results';
results.templateUrl = viewsPath + 'results.html';
results.controller = 'ResultsCtrl';
states.push(results);

var related = {}
related.name = 'results.related';
related.url = '/related/{doc_id}';
related.parent = results;
related.templateUrl = viewsPath + 'related.html';
related.controller = 'RelatedCtrl';
states.push(related);


angular.module('angularApp', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ui.router',
  'ui.router.stateHelper'
])
.config(function ($stateProvider, $urlRouterProvider,  $resourceProvider) {
  //delete $httpProvider.defaults.headers.common['X-Requested-With'];
  $urlRouterProvider.otherwise('/home');
  for(var i = 0; i < states.length; i++){
      $stateProvider.state(states[i]);
  }
  // $resourceProvider.defaults.stripTrailingSlashes = false;
})
.factory('Search', function($resource){
  return $resource("/api/async/v1/");
})
.factory('SearchResult', function($resource){
  return $resource("/api/async/v1/results/:id");
})
.filter('to_trusted', ['$sce', function($sce){
    return function(text) {
        return $sce.trustAsHtml(text);
    };
}])
.run(['$rootScope','$sce', '$state', function($rootScope, $sce, $state){
    $rootScope.$state = $state;
}]);




