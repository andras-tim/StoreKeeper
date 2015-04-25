'use strict';

/* Services */

var appServices = angular.module('appServices', []);

appServices.factory('Session', ['Restangular',
    function (Restangular) {
        return Restangular.service('sessions');
    }]);
