'use strict';

var appServices = angular.module('appServices', []);


appServices.factory('SessionService', function (Restangular) {
    return Restangular.service('sessions');
});
