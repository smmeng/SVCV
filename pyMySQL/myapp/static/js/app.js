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

//http://ui-grid.info/docs/#/tutorial/206_exporting_data
app = angular.module('appInvestorProfit', ['ngAnimate', 'ngTouch', 'ui.grid', 'ui.grid.selection', 'ui.grid.exporter']);

app.controller('MainCtrl', ['$scope', '$http', function ($scope, $http) {
	console.log("MainCtrl()	");
  $scope.gridOptions = {
    columnDefs: [
		{ field: 'UserId__username' },
		{ field: 'UserId__first_name', visible: true},
		{ field: 'UserId__last_name', visible: true},
		{ field: 'Amount__sum' },
		{ field: 'depositedEquityAmount', visible: false },
		{ field: 'returnEquityAmount' },
		{ field: 'remainingEquityAmount' },
    ],
    enableGridMenu: true,
    enableSelectAll: true,
    exporterCsvFilename: 'myFile.csv',
    exporterPdfDefaultStyle: {fontSize: 9},
    exporterPdfTableStyle: {margin: [30, 30, 30, 30]},
    exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
    exporterPdfHeader: { text: "My Header", style: 'headerStyle' },
    exporterPdfFooter: function ( currentPage, pageCount ) {
      return { text: currentPage.toString() + ' of ' + pageCount.toString(), style: 'footerStyle' };
    },
    exporterPdfCustomFormatter: function ( docDefinition ) {
      docDefinition.styles.headerStyle = { fontSize: 22, bold: true };
      docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
      return docDefinition;
    },
    exporterPdfOrientation: 'portrait',
    exporterPdfPageSize: 'LETTER',
    exporterPdfMaxGridWidth: 500,
    exporterCsvLinkElement: angular.element(document.querySelectorAll(".custom-csv-link-location")),
    onRegisterApi: function(gridApi){
      $scope.gridApi = gridApi;
    }
  };
 
  $http.get('/investorProfitsJSON/').success(function(data) {
	  
	$scope.summary = data;
  	// no first row for header
	
	console.log("table rows="+$scope.summary.length);
  	for(var i = 0; i < $scope.summary.length; i++)
  	{
  		row = $scope.summary[i];
  		col = ''
  		console.log("table columns="+row.length + " row="+data[1,1]);
  		
  		for(var j = 0; j < row.length; j++)
	    	{
  			col += row[j] + ", ";
  			
  			if (angular.isNumber(row[j]))
  				column =row[j];

  				row[j]= $filter('currency')(column).slice(0, -3);

  				console.log("table row["+i+"] "  + row[0] + "= " + column + " final value="+row[j]);
	    	}
  		console.log(col);
  	}

  	// construct last row for grand total
  	$scope.grandTotalRow = data[ $scope.summary.length - 1];
  	console.log("Total: " + $scope.grandTotalRow);
  	data.splice($scope.summary.length - 1, 1);
  	$scope.summary = data;
  	
	// Final Display
    $scope.gridOptions.data = data;
  });
 
}]);
