'use strict';

var appResourceFactories = angular.module('appFactories.resources', []);


appResourceFactories.factory('ConfigFactory', ['$q', 'Restangular', 'ConfigService',
    function ConfigFactory ($q, Restangular, ConfigService) {
        var
            config = {
                'app_name': undefined,
                'app_title': undefined,
                'forced_language': undefined,
                'debug': false
            },
            gettingConfigPromise;

        function getConfig() {
            if (config.app_name !== undefined) {
                return $q.when(config);
            }

            if (angular.isDefined(gettingConfigPromise)) {
                return gettingConfigPromise;
            }

            gettingConfigPromise = ConfigService.one().get().then(function (resp) {
                config = Restangular.stripRestangular(resp);
                return config;
            });
            return gettingConfigPromise;
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


appResourceFactories.factory('BarcodeCacheFactory', ['$q', 'Restangular', 'CommonFactory', 'BarcodeService',
    function BarcodeCacheFactory ($q, Restangular, CommonFactory, BarcodeService) {
        var
            BarcodeCache = function BarcodeCache (spinner) {
                var barcodeCache,
                    gettingBarcodesPromise,

                    getBarcodes = function getBarcodes () {
                        var result = $q.defer();

                        if (angular.isDefined(barcodeCache)) {
                            result.resolve(barcodeCache);
                            return result.promise;
                        }

                        if (angular.isDefined(gettingBarcodesPromise)) {
                            return gettingBarcodesPromise;
                        }

                        CommonFactory.handlePromise(
                            BarcodeService.getList(),
                            spinner,
                            function (barcodes) {
                                barcodeCache = Restangular.stripRestangular(barcodes);
                                result.resolve(barcodeCache);
                            });

                        gettingBarcodesPromise = result.promise;
                        return result.promise;
                    },

                    getBarcode = function getBarcode (barcodeValue) {
                        var result = $q.defer();

                        getBarcodes().then(function (barcodes) {
                            var index = _.findIndex(barcodes, 'barcode', barcodeValue);

                            if (index === -1) {
                                result.reject(barcodeValue);
                                return;
                            }

                            result.resolve(barcodes[index]);
                        });

                        return result.promise;
                    };

                return {
                    'getBarcode': getBarcode
                };
            };

        return BarcodeCache;
    }]);


appResourceFactories.factory('ItemCacheFactory', ['$q', 'Restangular', 'CommonFactory', 'ItemService',
    function ItemCacheFactory ($q, Restangular, CommonFactory, ItemService) {
        var
            ItemCache = function ItemCache (spinner) {
                var itemCache = {},

                    getItemById = function getItemById (itemId) {
                        var result = $q.defer();

                        if (angular.isDefined(itemCache[itemId])) {
                            result.resolve(itemCache[itemId]);
                            return result.promise;
                        }

                        CommonFactory.handlePromise(
                            ItemService.one(itemId).get(),
                            spinner,
                            function (item) {
                                itemCache[itemId] = item;
                                result.resolve(item);
                            },
                            function () {
                                result.reject();
                            }
                        );
                        return result.promise;
                    };

                return {
                    'getItemById': getItemById
                };
            };

        return ItemCache;
    }]);


appResourceFactories.factory('ElementDataFactory', ['ItemService',
    function ElementDataFactory (ItemService) {
        function itemPromise(elementId) {
            return ItemService.one(elementId).get();
        }

        return {
            'item': itemPromise
        };
    }]);
