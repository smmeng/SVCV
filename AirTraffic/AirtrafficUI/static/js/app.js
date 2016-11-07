var app = angular.module('appGMaps', []);

app.controller('appGMapsCtrl', function($scope, $filter, $http) {
	var jsonURL = "/showRouteData/";
	var homeLatlng = new google.maps.LatLng(37.3522374, -122.052706);
	$scope.mapProp = {
			    center:homeLatlng,
			    zoom:12,
			    mapTypeId:google.maps.MapTypeId.ROADMAP
			   };

	$scope.map=new google.maps.Map(document.getElementById("map_canvas"),$scope.mapProp);
	
    $http.get(jsonURL).success(function (data) {
    	$scope.summary = data;
    	
    	for(var i = 0; i < $scope.summary.length; i++)
    	{
    		row = $scope.summary[i];
    		console.log("row " + i  + "-" + row[0] + "-" + row[1][0]['lat'] + "-" + row[1][0]['lon'] );
    		var arrayCoords = [];
    		for (var alt = 0; alt < row[1].length; alt++)
			{
    			var latlong=  new google.maps.LatLng(row[1][alt]['lat'] , row[1][alt]['lon'] );
    			arrayCoords.push(latlong);
			}
    		
    		// draw the route on the map            
            var route = new google.maps.Polyline({
                path: arrayCoords,
                strokeColor: "blue",
                strokeOpacity: 1.0,
                strokeWeight: 1,
                geodesic: false,
                map: $scope.map
            }); 
            route.setMap($scope.map);
    	}
    	
    	console.log("Total: " + $scope.summary.length);
    });
});

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

app = angular.module('appInvestmentActivity', ['ngAnimate', 'ngTouch', 'ui.grid',  'ui.grid.grouping', 'ui.grid.selection', 'ui.grid.exporter']);

app.controller('appInvestmentActivityCtrl', ['$scope', 'uiGridConstants','$http', function ($scope, uiGridConstants, $http) {
	console.log("inside InvestmentActivity()	");
	
  $scope.gridOptions = {
    enableFiltering: false,
    treeRowHeaderAlwaysVisible: true,
    showGridFooter: true,
    showColumnFooter: true,
    columnDefs: [
		{ field: 'Type', displayName: 'Type', visible: false, },
		{ field: 'Date', displayName: 'Date',  visible: true, cellTemplate: '<div ng-bind-html="COL_FIELD | trusted"></div>'},
		{ field: 'ProjectStatus', displayName: 'Status', visible: true, cellTemplate: '<div ng-bind-html="COL_FIELD | trusted"></div>'},
		{ field: 'ProjectId_id', displayName: 'Project',  visible: true,  
			grouping: { groupPriority: 0 }, sort: { priority: 0, direction: 'desc' },
			cellTemplate: '<div ng-bind-html="COL_FIELD | trusted"><div ng-if="!col.grouping || col.grouping.groupPriority === undefined || col.grouping.groupPriority === null || ( row.groupHeader && col.grouping.groupPriority === row.treeLevel )" class="ui-grid-cell-contents" title="TOOLTIP">{{COL_FIELD CUSTOM_FILTERS}}</div></div>'},
		{ field: 'Memo', displayName: 'Description',  visible: true, cellTemplate: '<div ng-bind-html="COL_FIELD | trusted"></div>'},
		{ field: 'Principal', displayName: 'Principal', aggregationType: uiGridConstants.aggregationTypes.sum },
		{ field: 'Distribution', displayName: 'Distribution', aggregationType: uiGridConstants.aggregationTypes.sum},
		{ field: 'Interest', displayName: 'Interest', aggregationType: uiGridConstants.aggregationTypes.sum},
		{ field: 'Dividend', displayName: 'Dividend', aggregationType: uiGridConstants.aggregationTypes.sum},

    ],
/**    
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
    **/
  };
 
  /**
  $scope.selectInvestorId = function(investorId)
  {
	  alert("id");
	  console.log("id="+investorId);
  };**/
  
  $http.get('/restapi/investmentActivity/').success(function(data) {  	
	// Final Display
    
    $scope.summary = data;
    console.log("Total rows: " + $scope.summary.length);
    //console.log("First rows: " + $scope.summary[0]['Type']);
    $scope.principal=0;
    $scope.distribution=0;
    $scope.interest=0;
    $scope.dividend=0;
    for(var i = 0; i < $scope.summary.length; i++)
	{
		row = $scope.summary[i];
		if (row['ProjectStatus']=="Completed")
		{
			row['ProjectId_id'] ='<strike><bold><color="green">' + row['ProjectId_id'] + '</color></bold></strike>';
			//row['Type'] ='<strike>' + row['Type'] + '</strike>';
			row['Date'] ='<strike>' + row['Date'] + '</strike>';
			row['ProjectStatus'] ='<strike>' + row['ProjectStatus'] + '</strike>';
			row['Memo'] ='<strike>' + row['Memo'] + '</strike>';
		};

		if (row['Type'] =='Deposit')
		{
		    $scope.principal+=row['Amount'];
			row['Principal'] = row['Amount'];
		}
		else if (row['Type'] =='Check')
		{
			$scope.distribution+=row['Amount'];
			row['Distribution'] = row['Amount'];
		}
    	else if (row['Type'] =='Interest')
		{
    		$scope.interest+=row['Amount'];
    		row['Interest'] = row['Amount'];
  		}
  		else if (row['Type'] =='Dividend')
		{
  			$scope.dividend +=row['Amount'];
  			row['Dividend'] = row['Amount'];
		};
	};
		
	//console.log(i + " type="+ row['Type']);
	
	$scope.final_principal = $scope.principal + $scope.distribution;
	console.log("final amount="+ $scope.final_principal +" "+ $scope.principal +" "+ $scope.distribution);
    
    $scope.gridOptions.data = $scope.summary;

  });
  $scope.expandAll = function(){
	    $scope.gridApi.treeBase.expandAllRows();
	  };
	 
	  $scope.toggleRow = function( rowNum ){
	    $scope.gridApi.treeBase.toggleRowTreeState($scope.gridApi.grid.renderContainers.body.visibleRowCache[rowNum]);
	  };
	 
	  $scope.changeGrouping = function() {
	    $scope.gridApi.grouping.clearGrouping();
	    $scope.gridApi.grouping.groupColumn('Amount');
	    $scope.gridApi.grouping.aggregateColumn('ProjectId_id', uiGridGroupingConstants.aggregation.COUNT);
	  };
	 
	  $scope.getAggregates = function() {
	    var aggregatesTree = [];
	    var gender
	 
	    var recursiveExtract = function( treeChildren ) {
	      return treeChildren.map( function( node ) {
	        var newNode = {};
	        angular.forEach(node.row.entity, function( attributeCol ) {
	          if( typeof(attributeCol.groupVal) !== 'undefined' ) {
	            newNode.groupVal = attributeCol.groupVal;
	            newNode.aggVal = attributeCol.value;
	          }
	        });
	        newNode.otherAggregations = node.aggregations.map( function( aggregation ) {
	          return { colName: aggregation.col.name, value: aggregation.value, type: aggregation.type };
	        });
	        if( node.children ) {
	          newNode.children = recursiveExtract( node.children );
	        }
	        return newNode;
	      });
	    }
	 
	    aggregatesTree = recursiveExtract( $scope.gridApi.grid.treeBase.tree );
	 
	    console.log(aggregatesTree);
	  };
}]);
app.filter('trusted', function ($sce) {
	  return function (value) {
	    return $sce.trustAsHtml(value);
	  }
	});