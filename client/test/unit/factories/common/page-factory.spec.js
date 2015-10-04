'use strict';

describe('Factories/Common: PageFactory', function () {
    var test;

    beforeEach(module('appFactories.common'));

    beforeEach(function () {
        test = this;

        var data = {
                'config': {
                    'app_name': 'storekeeper_test',
                    'app_title': 'StoreKeeperTest',
                    'debug': false,
                    'forced_language': 'hu'
                }
            },

            mocks = {
                'ConfigFactory': {
                    'getConfig': function () {
                        return test.$q.when(data.config);
                    }
                }
            },

            injectFactory = function () {
                module(function ($provide) {
                    $provide.value('ConfigFactory', mocks.ConfigFactory);
                });
                spyOn(mocks.ConfigFactory, 'getConfig').and.callThrough();

                inject(function ($injector, $q, $rootScope) {
                    test.$q = $q;
                    test.$rootScope = $rootScope;

                    test.PageFactory = $injector.get('PageFactory');
                });
            };

        this.mocks = mocks;
        this.injectFactory = injectFactory;
    });

    it('test getting window title before set page title', function () {
        this.injectFactory();

        expect(test.PageFactory.getWindowTitle()).toBe('');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(0);
    });

    it('test getting window title after set page title', function () {
        this.injectFactory();

        test.PageFactory.setPageTitle('foo');
        expect(test.PageFactory.getWindowTitle()).toBe('');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);

        test.$rootScope.$apply();
        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest - foo');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
        test.PageFactory.setPageTitle('foo');
    });

    it('test getting window title after set page title multiple times', function () {
        this.injectFactory();

        test.PageFactory.setPageTitle('foo');
        test.$rootScope.$apply();
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest - foo');

        test.PageFactory.setPageTitle('bar');
        test.$rootScope.$apply();
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest - bar');
    });

    it('test getting window title after reset page title', function () {
        this.injectFactory();

        test.PageFactory.setPageTitle();
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
        test.$rootScope.$apply();

        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
    });

    it('check getting window title will serve from cache when it was call multiple times', function () {
        this.injectFactory();

        test.PageFactory.setPageTitle('foo');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
        test.$rootScope.$apply();

        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest - foo');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);

        expect(test.PageFactory.getWindowTitle()).toBe('StoreKeeperTest - foo');
        expect(test.mocks.ConfigFactory.getConfig.calls.count()).toEqual(1);
    });
});
