'use strict';

describe('Services', function () {
    var test,
        services;

    beforeEach(module('appServices', 'restangular'));

    beforeEach(function () {
        test = this;

        var data = {
                'dummyResponse': ['foo']
            },

            injectFactory = function (serviceFactoryName) {
                installPromiseMatchers();

                inject(function ($injector, $httpBackend) {
                    test.$httpBackend = $httpBackend;
                    test.serviceFactory = $injector.get(serviceFactoryName);
                });
            };

        this.data = data;
        this.injectFactory = injectFactory;
    });

    describe('test status code handling of API services', function () {

        beforeEach(function () {
            test.entryPoint = null;
        });

        afterEach(function () {
            test.$httpBackend.verifyNoOutstandingExpectation();
            test.$httpBackend.verifyNoOutstandingRequest();
        });

        services = [
            {'service': 'BarcodeService', 'entryPoint': '/barcodes'},
            {'service': 'ConfigService', 'entryPoint': '/config'},
            {'service': 'ItemService', 'entryPoint': '/items'},
            {'service': 'SessionService', 'entryPoint': '/session'},
            {'service': 'UnitService', 'entryPoint': '/units'},
            {'service': 'VendorService', 'entryPoint': '/vendors'}
        ];

        describe('positive tests; returns with 200', function () {
            /*jshint -W083 */ //Disable warning for function created inside loop
            services.forEach(function (data) {

                it(data.service + '.one().get()', function () {
                    test.injectFactory(data.service);

                    test.requestHandler = test.$httpBackend.when('GET', data.entryPoint)
                        .respond(200, test.data.dummyResponse);

                    test.$httpBackend.expectGET(data.entryPoint);
                    var promise = test.serviceFactory.one().get();
                    test.$httpBackend.flush();

                    expect(promise).toBeResolvedWith(test.data.dummyResponse);
                });

            });
        });

        describe('negative tests; returns with 403', function () {
            /*jshint -W083 */ //Disable warning for function created inside loop
            services.forEach(function (data) {

                it(data.service + '.one().get()', function () {
                    test.injectFactory(data.service);

                    test.requestHandler = test.$httpBackend.when('GET', data.entryPoint)
                        .respond(403, test.data.dummyResponse);

                    test.$httpBackend.expectGET(data.entryPoint);
                    var promise = test.serviceFactory.one().get();
                    test.$httpBackend.flush();

                    expect(promise).toBeRejected();
                });
            });
        });
    });
});
