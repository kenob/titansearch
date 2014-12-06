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
  'ui.router.stateHelper',
  'ui.bootstrap.pagination',
  'autocomplete'
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
.factory('AutoComplete', function($resource){
  return $resource("/api/async/v1/suggest");
})
.factory('TwitterNearby', function($resource){
  return $resource("/api/async/v1/twitter_nearby");
})
.filter('addEllipsis', function () {
    return function (input, max) {
        if (input) {
            // Replace this with the real implementation
            if(input.length > max){
              while(!(/\s/.test(input.charAt(max)))){
                max++;
                if(max > input.length)
                {
                  return input;
                }
              }
              return input.substring(0, max) + ' ...';  
            }
            else{
              return input;
            }
        }
    }
})
.run(['$rootScope','$sce', '$state', 'Search', 'AutoComplete', 
    function($rootScope, $sce, $state, Search, AutoComplete, TwitterNearby){
            $rootScope.$state = $state;
            $rootScope.alerts = [];
            $rootScope.searchForm = {};
            $rootScope.searchForm.q = "";
            $rootScope.autoCompleteTerms = [];

            $rootScope.search = function(){
              var res = Search
                    .get($rootScope.searchForm, 
                      function(data){
                        $rootScope.searchResultObject = data;
                        $state.go('results',{},{reload : true});
                      });
            };

            $rootScope.completeTerm = function(typed){
              if(typed.length>1){
              var res = AutoComplete
                    .get({q:typed}, 
                      function(data){
                        if($rootScope.autoCompleteTerms!=data.results){
                          $rootScope.autoCompleteTerms = data.results;
                        }
              });
              }
            };
  }]);




