'use strict';


angular.module('angularApp')
  .controller('ResultsCtrl', function ($scope, $rootScope, $state, Search, SearchResult) {
	  							var searchParams = {};

							  	$scope.change =  function(){
							  		searchParams.page = $scope.current_page;
							  		searchParams.q = $rootScope.searchResultObject.query_term;
							    	var res = Search
							    				.get(searchParams,
										    		function(data){
										    			$rootScope.searchResultObject = data;
	  													refreshPage($rootScope.searchResultObject);
	   													console.log(data);
	  													// $state.reload();
					  							});
	  								};

	  							var refreshPage = function (resultObject){
							  			$scope.search_results = resultObject.search_results;
							  			$scope.error_message = resultObject.error_message;
							  			$scope.query_term = resultObject.query_term;
							  			$scope.page_title = "Search results for " + resultObject.query_term;
							  			$scope.current_page = resultObject.current_page;
							  			$scope.has_next = resultObject.has_next;
							  			$scope.has_previous = resultObject.has_previous;
							  			$scope.num_results = resultObject.num_results;
	  							};

	  							if(!$rootScope.searchResultObject){
	  								$state.go('home');
	  							}
	  							else{
	  									refreshPage($rootScope.searchResultObject);

							  	}

});
