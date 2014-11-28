'use strict';

angular.module('angularApp')
  .controller('RelatedCtrl', function ($scope, SearchResult, $stateParams) {
  	    	var res = SearchResult
    				.get({id:$stateParams.doc_id}, 
			    		function(data){
			    				$scope.currentArticle = data;
				  		});
  });
