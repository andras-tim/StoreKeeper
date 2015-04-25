'use strict';

var appServices = angular.module('appServices', []);


appServices.factory('SessionService', function (Restangular) {
    return Restangular.service('sessions');
});


appServices.factory('ConfigService', function (Restangular) {
    return Restangular.service('configs');
});
