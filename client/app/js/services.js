'use strict';

var appServices = angular.module('appServices', []);


appServices.factory('SessionService', function (Restangular) {
    return Restangular.service('session');
});


appServices.factory('ConfigService', function (Restangular) {
    return Restangular.service('config');
});


appServices.factory('ItemService', function (Restangular) {
    return Restangular.service('items');
});
