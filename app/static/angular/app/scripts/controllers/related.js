'use strict';

angular.module('angularApp')
  .controller('RelatedCtrl', function ($scope, SearchResult, $stateParams, TwitterNearby) {
  	    	var res = SearchResult
    				.get({id:$stateParams.doc_id}, 
			    		function(data){
			    				$scope.currentArticle = data;
			    				$scope.link_message = "View this article on wikipedia"
				  		});
  });
