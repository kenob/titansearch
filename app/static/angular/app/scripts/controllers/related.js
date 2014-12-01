'use strict';

angular.module('angularApp')
  .controller('RelatedCtrl', function ($scope, SearchResult, $stateParams, TwitterNearby) {
  			 $scope.nearby = {text: "Show nearby tweets", status_bool:false, param:"False"}
             $scope.toggleNearby = function(){
             	  var nearby = {text: "Show nearby tweets", status_bool:false, param:"False"};
             	  if($scope.nearby.status_bool){
             	  		nearby = {text: "Show All tweets", status_bool:true, param:"True"};
  			 			$scope.nearby = nearby;

             	  }
                  var res = TwitterNearby
                    .get({title:$scope.currentArticle.wiki_article.title[0], nearby:nearby.param},
                      function(data){
						  $scope.currentArticle.related_tweets = data.tweets;
                      });
              };
  	    	var res = SearchResult
    				.get({id:$stateParams.doc_id}, 
			    		function(data){
			    				$scope.currentArticle = data;
			    				$scope.link_message = "View this article on wikipedia"
				  		});
  });
