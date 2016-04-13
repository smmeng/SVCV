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

app.controller('appInvestorProfitCtrl', ['$scope', 'uiGridConstants','$http', function ($scope, uiGridConstants, $http) {
	console.log("MainCtrl()	");
	
  $scope.gridOptions = {
    showGridFooter: true,
    showColumnFooter: true,
    //enableFiltering: true,
    columnDefs: [
		{ field: 'UserId__username', displayName: 'User', visible: false},
		{ field: 'UserId__first_name', displayName: 'First Name',  visible: true},
		{ field: 'UserId__last_name', displayName: 'Last Name', visible: true},
		{ field: 'Amount__sum', displayName: 'Total Profit', aggregationType: uiGridConstants.aggregationTypes.sum },
		{ field: 'depositedEquityAmount', displayName: 'Total Investment', visible: false , aggregationType: uiGridConstants.aggregationTypes.sum},
		{ field: 'returnEquityAmount', displayName: 'Total Returned Equity', aggregationType: uiGridConstants.aggregationTypes.sum },
		{ field: 'remainingEquityAmount', displayName: 'Outstanding Equity', aggregationType: uiGridConstants.aggregationTypes.sum },
    ],
    enableGridMenu: true,
    enableSelectAll: true,
    exporterCsvFilename: 'InvestorProfit.csv',
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
	// Final Display
    $scope.gridOptions.data = data;
  });
 
}]);

app = angular.module('appInvestmentActivity', ['ngAnimate', 'ngTouch', 'ui.grid', 'ui.grid.selection', 'ui.grid.exporter']);

app.controller('appInvestmentActivityCtrl', ['$scope', 'uiGridConstants','$http', function ($scope, uiGridConstants, $http) {
	console.log("InvestmentActivity()	");
	
  $scope.gridOptions = {
    showGridFooter: true,
    showColumnFooter: true,
    //enableFiltering: true,
    columnDefs: [
		{ field: 'Type', displayName: 'Type', visible: false},
		{ field: 'Date', displayName: 'Date',  visible: true},
		{ field: 'ProjectStatus', displayName: 'Status', visible: true},
		{ field: 'ProjectId_id', displayName: 'Project',  visible: true},
		{ field: 'Memo', displayName: 'Description',  visible: true},
		{ field: 'Principal', displayName: 'Principal', aggregationType: uiGridConstants.aggregationTypes.sum },
		{ field: 'Distribution', displayName: 'Distribution', aggregationType: uiGridConstants.aggregationTypes.sum},
		{ field: 'Interest', displayName: 'Interest', aggregationType: uiGridConstants.aggregationTypes.sum },
		{ field: 'Dividend', displayName: 'Dividend', aggregationType: uiGridConstants.aggregationTypes.sum },

    ],
    enableGridMenu: true,
    enableSelectAll: true,
    exporterCsvFilename: 'InvestmentActivity.csv',
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
 
  $http.get('/restapi/investmentActivity2/').success(function(data) {  	
	// Final Display
    
    $scope.summary = data;
    console.log("Total rows: " + $scope.summary.length);
    //console.log("First rows: " + $scope.summary[0]['Type']);
    for(var i = 0; i < $scope.summary.length; i++)
	{
		row = $scope.summary[i];
		if (row['Type'] =='Deposit')
			row['Principal'] = row['Amount'];
		else if (row['Type'] =='Check')
			row['Distribution'] = row['Amount'];
		else if (row['Type'] =='Interest')
			row['Interest'] = row['Amount'];
		if (row['Type'] =='Dividend')
			row['Dividend'] = row['Amount'];
		
		//console.log(i + " type="+ row['Type']);
	}
    
    $scope.gridOptions.data = $scope.summary;

  });
 
}]);