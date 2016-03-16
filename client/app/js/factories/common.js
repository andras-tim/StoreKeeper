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
                getProperErrorMessage(resp)
            );
        }

        function getProperErrorMessage(response) {
            var statusText = response.statusText,
                data = response.data;

            if (response.status === 0 && statusText === '' && data === null) {
                return gettextCatalog.getString('Can not connect to server');
            }

            if (angular.isObject(response.data)) {
                if (angular.isDefined(response.data.message)) {
                    data = JSON.stringify(data.message);
                } else {
                    data = JSON.stringify(data);
                }
            }

            if (statusText) {
                statusText += '<br />';
            }

            return statusText + data;
        }

        function setSpinner(spinnerName, value) {
            if (spinnerName) {
                $rootScope[spinnerName] = value;
            }
        }

        function setFocus(parentObject) {
            $timeout(function setFocusTimeout () {
                var defaultObject = parentObject.$element.find('[autofocus]');
                if (angular.isDefined(defaultObject)) {
                    defaultObject.focus();
                }
            });
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

            delayMs = delayMs || $rootScope.appDefaults.delayedPromiseCallback.delayMs;

            return {
                'callback': callback,
                'cancel': cancel
            };
        }


        return {
            'showResponseError': showResponseError,
            'printToConsole': printToConsole,
            'setFocus': setFocus,
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


appCommonFactories.factory('FloatingObjectFactory', ['$rootScope', '$route', '$location', '$log', '$q', 'CommonFactory', 'ElementDataFactory',
    function FloatingObjectFactory ($rootScope, $route, $location, $log, $q, CommonFactory, ElementDataFactory) {
        function floatingObjectHandler(availableObjects, searchTemplate, objectConstructor, onHideEventName) {
            var objects = {};

            function loadObjects() {
                angular.forEach(availableObjects, function (defaultOptions, objectId) {
                    var options = angular.merge({},
                            defaultOptions, {
                                'id': objectId
                            }),
                        obj = objectConstructor(options);

                    obj.$promise.then(function () {
                        obj.$scope.floatingObjectId = objectId;
                    });

                    objects[objectId] = obj;
                });
            }

            function openObject(objectId, elementId, elementData) {
                var obj = getObjectById(objectId),
                    searchTag = sprintf(searchTemplate, objectId),
                    floatingsEnabled = !!$route.current.floatingsEnabled;

                if (!obj || !floatingsEnabled) {
                    $location.search(searchTag, null);
                    return;
                }
                if (angular.isUndefined(elementId)) {
                    elementId = '1';
                }

                setDataOnScope(obj, elementId, elementData).then(function () {
                    return obj.$promise;
                }).then(function () {
                    if (!obj.$isShown) {
                        obj.show();
                        if (elementId && obj.$options.saveState !== false) {
                            $location.search(searchTag, elementId);
                        }
                    }
                    CommonFactory.setFocus(obj);
                });
            }

            function closeObject(objectId) {
                var obj = getObjectById(objectId);

                if (!obj) {
                    return;
                }

                obj.$promise.then(obj.hide);
            }

            function setDataOnScope(obj, elementId, elementData) {
                var dataFactory;

                obj.$scope.elementId = elementId;

                if (angular.isDefined(elementData) || angular.isUndefined(obj.$options.dataFactory)) {
                    obj.$scope.elementData = elementData;
                    return $q.when();
                }

                dataFactory = ElementDataFactory[obj.$options.dataFactory];
                return CommonFactory.handlePromise(
                    dataFactory(elementId),
                    null,
                    function (data) {
                        obj.$scope.elementData = data;
                        return $q.when();
                    });
            }

            function getObjectById(objectId) {
                var obj = objects[objectId];

                if (angular.isUndefined(obj)) {
                    $log.error('Missing object ' + ' \'' + objectId + '\'');
                    return null;
                }

                return obj;
            }

            function onObjectHide(event, obj) {
                var searchTag = sprintf(searchTemplate, obj.$id);

                $location.search(searchTag, null);
            }

            function showHideObjectsProperly() {
                angular.forEach(objects, function (obj, objectId) {
                    var searchTag = sprintf(searchTemplate, objectId),
                        elementId = $location.search()[searchTag];

                    if (elementId && elementId !== '0') {
                        openObject(objectId, elementId);
                    } else if ((!elementId || elementId === '0') && obj.$isShown) {
                        obj.$promise.then(obj.hide);
                    }
                });
            }

            loadObjects();

            $rootScope.$on('$routeChangeSuccess', showHideObjectsProperly);
            $rootScope.$on(onHideEventName, onObjectHide);

            return {
                'open': openObject,
                'close': closeObject
            };
        }

        return floatingObjectHandler;
    }]);



appCommonFactories.factory('ModalFactory', ['$rootScope', '$modal', 'FloatingObjectFactory',
    function ModalFactory ($rootScope, $modal, FloatingObjectFactory) {
        return new FloatingObjectFactory($rootScope.modals, '%s', $modal, 'modal.hide');
    }]);


appCommonFactories.factory('SidebarFactory', ['$rootScope', '$aside', 'FloatingObjectFactory',
    function SidebarFactory ($rootScope, $aside, FloatingObjectFactory) {
        return new FloatingObjectFactory($rootScope.sidebars, '%s-sidebar', $aside, 'aside.hide');
    }]);


appCommonFactories.factory('ShortcutFactory', [
    function ShortcutFactory () {
        var
            shortcutHandler = function shortcutHandler (shortcuts) {
                function onKeyDown($event) {
                    var handler = shortcuts[$event.which];
                    if (angular.isUndefined(handler)) {
                        return;
                    }
                    handler();
                }

                return onKeyDown;
            };

        return shortcutHandler;
    }]);
