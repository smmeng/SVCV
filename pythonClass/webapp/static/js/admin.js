angular.module('routeApp', ['ngRoute'])
    .config(function($routeProvider){
        console.log("In $routeProvider ["+$routeProvider);
        $routeProvider.
            when('/visitorLog', {
            templateUrl:'/visitorLog/',
            controller:''
        }).when('/visitorType', {
            templateUrl:'/visitorType/',
            controller:''
        }).when('/employee', {
            templateUrl:'/employee/',
            controller:''
        }).otherwise({
            redirectTo:'/visitorLog'
        })
    })
/**
 * Created by smmeng on 6/8/2016.
 */
