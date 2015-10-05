'use strict';

var appCommonFactories = angular.module('appFactories.common', []);


appCommonFactories.factory('CommonFactory', ['$rootScope', '$q', '$timeout', '$alert', '$log', '$filter', 'gettextCatalog', 'ConfigFactory',
    function CommonFactory ($rootScope, $q, $timeout, $alert, $log, $filter, gettextCatalog, ConfigFactory) {
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

        function printToConsole(message, data) {
            if (ConfigFactory.getDebug()) {
                $log.debug(message, data);
            }
        }

        function showResponseError(resp) {
            $log.error(resp);
            showErrorPopup(
                gettextCatalog.getString('Error {{ status }}', {'status': resp.status}),
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

        function createDelayedPromiseCallback(promiseCallback, delayMs) {
            var previousQuery;

            function callback(argument) {
                var result = $q.defer();

                if (angular.isDefined(previousQuery)) {
                    previousQuery.reject();
                }
                previousQuery = result;

                $timeout(function () {
                    if (result.promise.$$state.status === 0) {
                        promiseCallback(argument).then(function (data) {
                            result.resolve(data);
                        }, function (data) {
                            result.reject(data);
                        });
                    }
                }, delayMs);

                return result.promise;
            }

            function cancel() {
                if (previousQuery) {
                    previousQuery.reject();
                }
            }

            delayMs = delayMs || 600;

            return {
                'callback': callback,
                'cancel': cancel
            };
        }


        return {
            'showResponseError': showResponseError,
            'printToConsole': printToConsole,
            'handlePromise': handlePromise,
            'createDelayedPromiseCallback': createDelayedPromiseCallback
        };
    }]);


appCommonFactories.factory('PageFactory', ['ConfigFactory',
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


appCommonFactories.factory('PersistFactory', ['CommonFactory',
    function PersistFactory (CommonFactory) {
        function load(name, version) {
            var storage = JSON.parse(localStorage.getItem(name)) || {};

            if (storage.version !== version) {
                CommonFactory.printToConsole('Persistent factory version mismatch; request=' + name + ':' + version, storage);
                storage = {
                    'version': version,
                    'data': {}
                };
            }

            return {
                'data': storage.data,
                'save': function () {
                    localStorage.setItem(name, JSON.stringify(storage));
                }
            };
        }

        return {
            'load': load
        };
    }]);

