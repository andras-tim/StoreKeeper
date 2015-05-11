'use strict';

var appServices = angular.module('appServices', []);


//appServices.factory('AcquisitionService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('acquisitions');
//    }]);


//appServices.factory('BarcodeService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('barcodes');
//    }]);


appServices.factory('ConfigService', ['Restangular',
    function (Restangular) {
        return Restangular.service('config');
    }]);


//appServices.factory('CustomerService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('customers');
//    }]);


appServices.factory('ItemService', ['Restangular',
    function (Restangular) {
        return Restangular.service('items');
    }]);


appServices.factory('SessionService', ['Restangular',
    function (Restangular) {
        return Restangular.service('session');
    }]);


//appServices.factory('StocktakingService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('stocktaking');
//    }]);


//appServices.factory('UnitService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('works');
//    }]);


//appServices.factory('VendorService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('vendors');
//    }]);


//appServices.factory('WorkService', ['Restangular',
//    function (Restangular) {
//        return Restangular.service('works');
//    }]);
