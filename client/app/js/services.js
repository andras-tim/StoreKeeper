'use strict';

var appServices = angular.module('appServices', []);


//appServices.factory('AcquisitionService', function (Restangular) {
//    return Restangular.service('acquisitions');
//});


//appServices.factory('BarcodeService', function (Restangular) {
//    return Restangular.service('barcodes');
//});


appServices.factory('ConfigService', function (Restangular) {
    return Restangular.service('config');
});


//appServices.factory('CustomerService', function (Restangular) {
//    return Restangular.service('customers');
//});


appServices.factory('ItemService', function (Restangular) {
    return Restangular.service('items');
});


appServices.factory('SessionService', function (Restangular) {
    return Restangular.service('session');
});


//appServices.factory('StocktakingService', function (Restangular) {
//    return Restangular.service('stocktaking');
//});


//appServices.factory('UnitService', function (Restangular) {
//    return Restangular.service('works');
//});


//appServices.factory('VendorService', function (Restangular) {
//    return Restangular.service('vendors');
//});


//appServices.factory('WorkService', function (Restangular) {
//    return Restangular.service('works');
//});
