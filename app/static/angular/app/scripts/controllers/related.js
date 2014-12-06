'use strict';

angular.module('angularApp')
  .controller('RelatedCtrl', function ($scope, SearchResult, $stateParams, TwitterNearby) {
		 $scope.nearby = {text: "Show Nearby tweets", status_bool:false, param:"False"}
     $scope.toggleNearby = function(){
     	  if($scope.nearby.status_bool){
     	  	$scope.nearby = {text: "Show All tweets", status_bool:false, param:"True"};
     	  }
     	  else{
     	  	$scope.nearby = {text: "Show Nearby tweets", status_bool:true, param:"False"};
     	  }
          var res = TwitterNearby
            .get({title:$scope.currentArticle.wiki_article.title[0], nearby:$scope.nearby.param},
              function(data){
				  $scope.currentArticle.related_tweets = data.tweets;
              });
      };
    	var res = SearchResult
			.get({id:$stateParams.doc_id}, 
	    		function(data){
	    				$scope.currentArticle = data;
	    				$scope.link_message = "View this article on wikipedia"
	    				for(var i=0; i < $scope.currentArticle.related_news.length; i++){
	    					if(!$scope.currentArticle.related_news[i].links){
	    						$scope.currentArticle.related_news[i].links = [];
	    						$scope.currentArticle.related_news[i].links.push('/reuters_news_page/' + $scope.currentArticle.related_news[i].id);
	    					}
	    				}
		  		});
  });
