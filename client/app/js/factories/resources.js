'use strict';

var appResourceFactories = angular.module('appFactories.resource', []);


appResourceFactories.factory('ConfigFactory', ['$q', 'Restangular', 'ConfigService',
    function ConfigFactory ($q, Restangular, ConfigService) {
        var config = {
            'app_name': undefined,
            'app_title': undefined,
            'forced_language': undefined,
            'debug': false
        };

        function getConfig() {
            if (config.app_name !== undefined) {
                return $q.when(config);
            }

            return ConfigService.one().get().then(function (resp) {
                config = Restangular.stripRestangular(resp);
                return config;
            });
        }

        function getDebug() {
                return config.debug;
            }

        return {
            'getConfig': getConfig,
            'getDebug': getDebug
        };
    }]);


appResourceFactories.factory('SessionFactory', ['$q', 'Restangular', 'SessionService', 'CommonFactory',
    function SessionFactory ($q, Restangular, SessionService, CommonFactory) {
        var session = {},
            initialized = false;

        function clearSession() {
            session = {
                'id': 0,
                'username': null,
                'email': null,
                'admin': false,
                'disabled': false
            };
        }

        function getSession() {
            var result = $q.defer();

            SessionService.one().get().then(function (resp) {
                session = Restangular.stripRestangular(resp);
                initialized = true;
                result.resolve(session);
            }, function (resp) {
                if (resp.status !== 401) {
                    CommonFactory.showResponseError(resp);
                }
                initialized = true;
                result.reject(session);
            });

            return result.promise;
        }

        function login(username, password, remember) {
            var result = $q.defer(),
                credentials = {
                    'username': username,
                    'password': password,
                    'remember': remember
                };

            SessionService.post(credentials).then(function (resp) {
                session = Restangular.stripRestangular(resp);
                initialized = true;
                result.resolve(session);
            }, function (resp) {
                CommonFactory.showResponseError(resp);
                result.reject(resp);
            });

            return result.promise;
        }

        function logout() {
            var result = $q.defer();

            SessionService.one().remove().then(function () {
                clearSession();
                result.resolve(session);
            }, function (resp) {
                if (resp.status === 401) {
                    clearSession();
                    result.resolve(session);
                } else {
                    CommonFactory.showResponseError(resp);
                    result.reject(resp);
                }
            });

            return result.promise;
        }

        function getCachedSession() {
            if (!initialized) {
                return getSession();
            }

            return $q(function (resolve, reject) {
                if (session.username === null) {
                    reject(session);
                } else {
                    resolve(session);
                }
            });
        }

        function isAuthenticated() {
            if (!initialized) {
                return false;
            }
            return session.username !== null;
        }

        clearSession();
        return {
            'isAuthenticated': isAuthenticated,
            'getSession': getCachedSession,
            'login': login,
            'logout': logout
        };
    }]);
