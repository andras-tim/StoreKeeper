'use strict';

describe('ConfigFactory', function () {
    var test;

    beforeEach(module('storekeeperApp'));

    beforeEach(inject(function ($injector, $http, $httpBackend) {
        test = this;

        test.$httpBackend = $httpBackend;

        var afterInjects = [],

            data = {
                'valid_config': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'hu'
                },
                'valid_config_w_debug': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': true,
                    'forced_language': 'hu'
                },
                'invalid_config': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest'
                }
            },

            injectFactory = function () {
                test.ConfigFactory = $injector.get('ConfigFactory');

                afterInjects.forEach(function (afterInject) {
                    afterInject();
                });
            };

        this.afterInjects = afterInjects;
        this.data = data;
        this.injectFactory = injectFactory;
    }));

    afterEach(function () {
        test.$httpBackend.verifyNoOutstandingExpectation();
        test.$httpBackend.verifyNoOutstandingRequest();
    });

    describe('getConfig()', function () {

        describe('call with valid config', function () {

            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.authRequestHandler = test.$httpBackend.when('GET', 'api/config')
                        .respond(test.data.valid_config);
                });
            });

            it('once', function () {
                this.injectFactory();

                test.$httpBackend.expectGET('api/config');
                test.ConfigFactory.getConfig().then(
                    function (data) {
                        expect(data).toEqual(test.data.valid_config);
                    }, function (data) {
                        expect(data).not.toBeDefined();
                    });
                test.$httpBackend.flush();
            });

            it('twice; the second have not to use http', function () {
                this.injectFactory();

                test.$httpBackend.expectGET('api/config');
                test.ConfigFactory.getConfig().then(
                    function (data) {
                        expect(data).toEqual(test.data.valid_config);
                    }, function (data) {
                        expect(data).not.toBeDefined();
                    });
                test.$httpBackend.flush();

                test.ConfigFactory.getConfig().then(
                    function (data) {
                        expect(data).toEqual(test.data.valid_config);
                    }, function (data) {
                        expect(data).not.toBeDefined();
                    });
            });
        });

        describe('call with invalid config', function () {

            beforeEach(function () {
                this.afterInjects.push(function () {
                    test.authRequestHandler = test.$httpBackend.when('GET', 'api/config')
                        .respond(test.data.invalid_config);
                });
            });

            it('do not drop error yet', function () {
                this.injectFactory();

                test.$httpBackend.expectGET('api/config');
                test.ConfigFactory.getConfig().then(
                    function (data) {
                        expect(data).toEqual(test.data.invalid_config);
                    }, function (data) {
                        expect(data).not.toBeDefined();
                    });
                test.$httpBackend.flush();
            });
        });

    });


    describe('getDebug()', function () {
        beforeEach(function () {
            this.afterInjects.push(function () {
                test.authRequestHandler = test.$httpBackend.when('GET', 'api/config')
                    .respond(test.data.valid_config_w_debug);
            });
        });

        it('can call before fetch config from server', function () {
            this.injectFactory();

            expect(test.ConfigFactory.getDebug()).toBeFalsy();
            test.$httpBackend.flush();
        });

        it('return value from config after fetch', function () {
            this.injectFactory();

            test.$httpBackend.expectGET('api/config');
            test.ConfigFactory.getConfig().then(
                function (data) {
                    expect(test.ConfigFactory.getDebug()).toBeTruthy();
                }, function (data) {
                    expect(data).not.toBeDefined();
                });
            test.$httpBackend.flush();
        });
    });

});
