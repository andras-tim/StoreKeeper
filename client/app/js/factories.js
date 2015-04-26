'use strict';

var appFactories = angular.module('appFactories', []);


appFactories.factory('HelperFactory', function ($alert, gettextCatalog, ConfigFactory) {
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
        if (ConfigFactory.getConfig().debug) {
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
});


appFactories.factory('ConfigFactory', function (ConfigService) {
    var config = {
        appName: undefined,
        appTitle: 'StoreKeeper',
        debug: true// set false after made it server side
    };

    ConfigService.one().get().then(function (resp) {
        config.appName = resp.app_name;
        config.appTitle = resp.app_title;
        // FIXME: make it server side config.debug = resp.debug;
    });

    return {
        getConfig: function () {
            return config;
        }
    }
});


appFactories.factory('PageFactory', function (ConfigFactory) {
    var appTitle = ConfigFactory.getConfig().appTitle;
    var windowTitle = appTitle;

    function getTitleSuffix(pageTitle) {
        if (pageTitle == undefined) {
            return '';
        }
        return ' - ' + pageTitle;
    }

    return {
        getWindowTitle: function () {
            return windowTitle
        },
        setPageTitle: function (newPageTitle) {
            windowTitle = appTitle + getTitleSuffix(newPageTitle);
        }
    };
});


appFactories.factory('SessionFactory', function ($q, Restangular, SessionService, HelperFactory) {
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

    function apiLogin(username, password) {
        var result = $q.defer();

        var credentials = { username: username, password: password };
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

    function getCachedSession() {
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

    clearSession();
    return {
        getSession: getCachedSession,
        login: apiLogin,
        logout: apiLogout
    };
});
