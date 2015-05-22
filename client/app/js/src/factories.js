'use strict';

var appFactories = angular.module('appFactories', []);


appFactories.factory('HelperFactory', ['$alert', 'gettextCatalog', 'ConfigFactory',
    function ($alert, gettextCatalog, ConfigFactory) {
        function showErrorPopup(title, content) {
            $alert({
                title: title,
                content: content,
                container: "body",
                placement: "top-right",
                type: "danger",
                duration: 10,
                show: true
            });
        }

        function printToConsole(data) {
            if (ConfigFactory.getDebug()) {
                console.debug(data);
            }
        }

        return {
            showResponseError: function (resp) {
                printToConsole(resp);
                showErrorPopup(
                    gettextCatalog.getString("Error {{status}}", {status: resp.status}),
                    resp.statusText + "<br />" + resp.data
                );
            },
            printToConsole: printToConsole
        }
    }]);


appFactories.factory('ConfigFactory', ['$q', 'Restangular', 'ConfigService',
    function ($q, Restangular, ConfigService) {
        var config = {
            app_name: undefined,
            app_title: undefined,
            forced_language: undefined,
            debug: false
        };

        function apiGetConfig() {
            var result = $q.defer();

            if (config.app_name != undefined) {
                result.resolve(config);
            } else {
                ConfigService.one().get().then(function (resp) {
                    config = Restangular.stripRestangular(resp);
                    result.resolve(config);
                }, function (resp) {
                    HelperFactory.showResponseError(resp);
                    result.reject(config);
                });
            }

            return result.promise;
        }

        return {
            getConfig: apiGetConfig,
            getDebug: function () {
                return config.debug;
            }
        }
    }]);


appFactories.factory('PageFactory', ['ConfigFactory',
    function (ConfigFactory) {
        var appTitle;
        var windowTitle;

        function getTitleSuffix(pageTitle) {
            if (pageTitle == undefined) {
                return '';
            }
            return ' - ' + pageTitle;
        }

        function setPageTitle(newPageTitle) {
            if (appTitle != undefined) {
                windowTitle = appTitle + getTitleSuffix(newPageTitle);
                return
            }
            ConfigFactory.getConfig().then(function (config) {
                appTitle = config.app_title;
                windowTitle = appTitle + getTitleSuffix(newPageTitle);
            });
        }

        return {
            getWindowTitle: function () { return windowTitle },
            setPageTitle: setPageTitle
        };
    }]);


appFactories.factory('SessionFactory', ['$q', 'Restangular', 'SessionService', 'HelperFactory',
    function ($q, Restangular, SessionService, HelperFactory) {
        var session = {};
        var initialized = false;

        function clearSession() {
            session = {
                id: 0,
                username: null,
                email: null,
                admin: false,
                disabled: false
            };
        }

        function apiGetSession() {
            var result = $q.defer();

            SessionService.one().get().then(function (resp) {
                session = Restangular.stripRestangular(resp);
                initialized = true;
                result.resolve(session);
            }, function (resp) {
                if (resp.status == 401) {
                    clearSession();
                } else {
                    HelperFactory.showResponseError(resp);
                }
                initialized = true;
                result.reject(resp);
            });

            return result.promise;
        }

        function apiLogin(username, password, remember) {
            var result = $q.defer();

            var credentials = { username: username, password: password, remember: remember };
            SessionService.post(credentials).then(function (resp) {
                session = Restangular.stripRestangular(resp);
                result.resolve(session);
            }, function (resp) {
                HelperFactory.showResponseError(resp);
                result.reject(resp);
            });

            return result.promise;
        }

        function apiLogout() {
            var result = $q.defer();

            SessionService.one().remove().then(function () {
                clearSession();
                result.resolve(session);
            }, function (resp) {
                if (resp.status == 401) {
                    clearSession();
                    result.resolve(session);
                } else {
                    HelperFactory.showResponseError(resp);
                    result.reject(resp);
                }
            });

            return result.promise;
        }

        function apiGetCachedSession() {
            if (!initialized) {
                return apiGetSession();
            }

            return $q(function(resolve, reject) {
                if (session.username == null) {
                    reject(session);
                } else {
                    resolve(session);
                }
            });
        }

        function apiIsAuthenticated() {
            if (!initialized) {
                return false;
            }
            return session.username != null;
        }

        clearSession();
        return {
            isAuthenticated: apiIsAuthenticated,
            getSession: apiGetCachedSession,
            login: apiLogin,
            logout: apiLogout
        };
    }]);
