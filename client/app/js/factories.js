'use strict';

var appFactories = angular.module('appFactories', []);


appFactories.factory('CommonFactory', ['$rootScope', '$alert', '$log', '$filter', 'gettextCatalog', 'ConfigFactory',
    function CommonFactory ($rootScope, $alert, $log, $filter, gettextCatalog, ConfigFactory) {
        function showErrorPopup(title, content) {
            $alert({
                'title': title,
                'content': content,
                'container': 'body',
                'placement': 'top-right',
                'type': 'danger',
                'duration': 10,
                'show': true
            });
        }

        function printToConsole(data) {
            if (ConfigFactory.getDebug()) {
                $log.debug(data);
            }
        }

        function showResponseError(resp) {
            $log.error(resp);
            showErrorPopup(
                gettextCatalog.getString('Error {{status}}', {'status': resp.status}),
                resp.statusText + '<br />' + resp.data
            );
        }

        function setSpinner(spinnerName, value) {
            if (spinnerName) {
                $rootScope[spinnerName] = value;
            }
        }

        function handlePromise(promise, spinnerName, doneFunc, errorFunc) {
            setSpinner(spinnerName, true);

            promise.then(function (resp) {
                if (doneFunc) {
                    doneFunc(resp);
                }
                setSpinner(spinnerName, false);
            }, function (resp) {
                if (errorFunc) {
                    errorFunc(resp);
                }
                showResponseError(resp);
                setSpinner(spinnerName, false);
            });

            return promise;
        }

        function getObjectById(objects, id) {
            var objectId = parseInt(id),
                results;

            if (objectId) {
                results = $filter('filter')(objects, {'id': objectId}, true);
                if (results.length === 1) {
                    return results[0];
                }
            }
            return null;
        }

        return {
            'showResponseError': showResponseError,
            'printToConsole': printToConsole,
            'handlePromise': handlePromise,
            'getObjectById': getObjectById
        };
    }]);


appFactories.factory('ConfigFactory', ['$q', 'Restangular', 'ConfigService',
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


appFactories.factory('PageFactory', ['ConfigFactory',
    function PageFactory (ConfigFactory) {
        var appTitle,
            windowTitle = '';

        function getTitleSuffix(pageTitle) {
            if (pageTitle === undefined) {
                return '';
            }
            return ' - ' + pageTitle;
        }

        function setPageTitle(newPageTitle) {
            if (appTitle !== undefined) {
                windowTitle = appTitle + getTitleSuffix(newPageTitle);
                return;
            }
            ConfigFactory.getConfig().then(function (config) {
                appTitle = config.app_title;
                windowTitle = appTitle + getTitleSuffix(newPageTitle);
            });
        }

        function getWindowTitle() {
            return windowTitle;
        }

        return {
            'getWindowTitle': getWindowTitle,
            'setPageTitle': setPageTitle
        };
    }]);


appFactories.factory('SessionFactory', ['$q', 'Restangular', 'SessionService', 'CommonFactory',
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
