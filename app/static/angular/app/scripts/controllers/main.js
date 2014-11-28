'use strict';

angular.module('angularApp')
  .controller('MainCtrl', function ($rootScope, $state, Search, $scope) {
  	$scope.searchForm = {};
    $scope.search = function(){
    	var res = Search
    				.get($scope.searchForm, 
			    		function(data){
			    			$rootScope.searchResultObject = data;
			    			console.log(data);
    						$state.go('results');
				  		});
  	};
  	});
