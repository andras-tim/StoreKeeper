'use strict';

describe('ConfigFactory', function () {
    var test;

    beforeEach(module('appFactories'));

    beforeEach(function () {
        test = this;

        var afterInjects = [],

            data = {
                'validConfig': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'hu'
                },
                'validConfigWithDebug': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': true,
                    'forced_language': 'hu'
                },
                'invalidConfig': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest'
                }
            },

            mocks = {
                'ConfigService': {
                    'one': function () {
                        return this;
                    },
                    'get': function () {
                        return helper.promiseMock(test, 'resultsResolved', test.results, test.results);
                    }
                },
                'Restangular': {
                    'stripRestangular': function (data) {
                        return data;
                    }
                }
            },

            injectFactory = function () {
                module(function ($provide) {
                    $provide.value('ConfigService', mocks.ConfigService);
                    $provide.value('Restangular', mocks.Restangular);
                });
                spyOn(mocks.ConfigService, 'get').and.callThrough();

                installPromiseMatchers();

                inject(function ($injector, $q) {
                    test.$q = $q;
                    test.ConfigFactory = $injector.get('ConfigFactory');
                });

                afterInjects.forEach(function (afterInject) {
                    afterInject();
                });
            };

        this.afterInjects = afterInjects;
        this.data = data;
        this.mocks = mocks;
        this.injectFactory = injectFactory;
    });

    beforeEach(function () {
        this.afterInjects.push(function () {
            test.results = null;
            test.resultsResolved = true;
        });
    });

    describe('getConfig()', function () {

        describe('get valid config', function () {

            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.results = test.data.validConfig;
                });
            });

            it('once', function () {
                var promise;
                this.injectFactory();

                promise = test.ConfigFactory.getConfig();
                expect(promise).toBeResolvedWith(test.data.validConfig);
                expect(test.mocks.ConfigService.get.calls.count()).toEqual(1);
            });

            it('twice; the second have not to use http', function () {
                var promise;
                this.injectFactory();

                promise = test.ConfigFactory.getConfig();
                expect(promise).toBeResolvedWith(test.data.validConfig);
                expect(test.mocks.ConfigService.get.calls.count()).toEqual(1);

                promise = test.ConfigFactory.getConfig();
                expect(promise).toBeResolvedWith(test.data.validConfig);
                expect(test.mocks.ConfigService.get.calls.count()).toEqual(1);
            });
        });

        describe('get invalid config', function () {

            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.results = test.data.invalidConfig;
                });
            });

            it('do not drop error yet', function () {
                var promise;
                this.injectFactory();

                promise = test.ConfigFactory.getConfig();
                expect(promise).toBeResolvedWith(test.data.invalidConfig);
            });
        });

        describe('get invalid response', function () {

            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.resultsResolved = false;
                });
            });

            it('do not drop error yet', function () {
                var promise;
                this.injectFactory();

                promise = test.ConfigFactory.getConfig();
                expect(promise).toBeRejected();
            });
        });
    });

    describe('getDebug()', function () {

        beforeEach(function () {
            this.afterInjects.push(function () {
                test.results = test.data.validConfigWithDebug;
            });
        });

        it('can call before fetch config from server', function () {
            var debug;
            this.injectFactory();

            debug = test.ConfigFactory.getDebug();
            expect(debug).toBeFalsy();
            expect(test.mocks.ConfigService.get.calls.count()).toEqual(0);
        });

        it('return value from config after fetch', function () {
            var promise,
                debug;
            this.injectFactory();

            promise = test.ConfigFactory.getConfig();
            expect(promise).toBeResolvedWith(test.data.validConfigWithDebug);
            expect(test.mocks.ConfigService.get.calls.count()).toEqual(1);

            debug = test.ConfigFactory.getDebug();
            expect(debug).toBeTruthy();
            expect(test.mocks.ConfigService.get.calls.count()).toEqual(1);
        });
    });
});
