var app = angular.module('myApp', ['anguFixedHeaderTable']);

app.controller('projectInvestorSummarysCtrl', function($scope, $filter, $http) {
	var jsonURL = "/projectInvestorSummaryData/";
	
	//$scope.summary = [];
    $http.get(jsonURL).success(function (data) {
    	$scope.summary = data;
    	// construct first row for header
    	$scope.colName = $scope.summary[0];
    	console.log("Headers: " + $scope.colName);
    	data.splice(0, 1);
    	$scope.summary = data;
    	
    	for(var i = 0; i < $scope.summary.length; i++)
    	{
    		row = $scope.summary[i];
    		col = ''
    		for(var j = 0; j < row.length; j++)
	    	{
    			col += row[j] + ", ";
    			
    			if (angular.isNumber(row[j]))
    				row[j]= $filter('currency')(row[j]).slice(0, -3);
	    	}
    		//console.log(col);
    	}

    	// construct last row for grand total
    	$scope.grandTotalRow = data[ $scope.summary.length - 1];
    	console.log("Total: " + $scope.grandTotalRow);
    	data.splice($scope.summary.length - 1, 1);
    	$scope.summary = data;
    	
            
    });
    
        
   
});


