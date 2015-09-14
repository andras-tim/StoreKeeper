'use strict';

describe('Factories: CommonFactory', function () {
    var test;

    beforeEach(module('appFactories'));

    beforeEach(function () {
        test = this;

        var afterInjects = [],

            data = {
                'badResponse': {
                    'status': '404',
                    'statusText': 'foo',
                    'data': 'bar'
                }
            },

            mocks = {
                '$alert': function () {},
                'filterFilter': function () {
                    return test.filterResults;
                },
                '$filter': function () {
                    return mocks.filterFilter;
                },
                'gettextCatalog': {
                    'getString': function (string) {
                        return string;
                    }
                },
                'ConfigFactory': {
                    'getDebug': function () {
                        return test.debugMode;
                    }
                }
            },

            injectFactory = function () {
                module(function ($provide) {
                    $provide.value('$alert', mocks.$alert);
                    $provide.value('$filter', mocks.$filter);
                    $provide.value('gettextCatalog', mocks.gettextCatalog);
                    $provide.value('ConfigFactory', mocks.ConfigFactory);
                });
                spyOn(mocks, '$alert').and.stub();
                spyOn(mocks, 'filterFilter').and.callThrough();

                inject(function ($injector, $rootScope, $log, $q) {
                    test.$rootScope = $rootScope;
                    test.$log = $log;
                    test.$q = $q;

                    test.CommonFactory = $injector.get('CommonFactory');
                });

                afterInjects.forEach(function (afterInject) {
                    afterInject();
                });
            };

        this.data = data;
        this.afterInjects = afterInjects;
        this.mocks = mocks;
        this.injectFactory = injectFactory;
    });

    describe('printToConsole()', function () {

        it('do not print anything in non debug mode', function () {
            test.injectFactory();
            test.debugMode = false;

            test.CommonFactory.printToConsole('foo');

            expect(test.$log.log.logs).toEqual([]);
            expect(test.$log.info.logs).toEqual([]);
            expect(test.$log.warn.logs).toEqual([]);
            expect(test.$log.error.logs).toEqual([]);
            expect(test.$log.debug.logs).toEqual([]);
        });

        it('do print debug log in debug mode', function () {
            test.injectFactory();
            test.debugMode = true;

            test.CommonFactory.printToConsole('foo');

            expect(test.$log.log.logs).toEqual([]);
            expect(test.$log.info.logs).toEqual([]);
            expect(test.$log.warn.logs).toEqual([]);
            expect(test.$log.error.logs).toEqual([]);
            expect(test.$log.debug.logs).toEqual([['foo']]);
        });

    });

    describe('showResponseError()', function () {

        beforeEach(function () {
            test.response = test.data.badResponse;
        });

        it('display response in console log and in a popup message', function () {
            test.injectFactory();

            test.CommonFactory.showResponseError(test.response);

            expect(test.$log.log.logs).toEqual([]);
            expect(test.$log.info.logs).toEqual([]);
            expect(test.$log.warn.logs).toEqual([]);
            expect(test.$log.error.logs).toEqual([[test.response]]);
            expect(test.$log.debug.logs).toEqual([]);

            expect(test.mocks.$alert).toHaveBeenCalledWith({
                'title': 'Error {{status}}',
                'content': 'foo<br />bar',
                'container': 'body',
                'placement': 'top-right',
                'type': 'danger',
                'duration': 10,
                'show': true
            });
        });

    });

    describe('handlePromise()', function () {

        beforeEach(function () {
            this.afterInjects.push(function () {
                test.deferred = test.$q.defer();
                test.promise = test.deferred.promise;
            });
        });

        describe('with resolved promise', function () {

            it('check spinner visibility', function () {
                test.injectFactory();

                expect(test.$rootScope.testSpinner).not.toBeDefined();

                test.CommonFactory.handlePromise(test.promise, 'testSpinner');
                expect(test.$rootScope.testSpinner).toBeDefined();
                expect(test.$rootScope.testSpinner).toBeTruthy();

                test.deferred.resolve();
                test.$rootScope.$apply();

                expect(test.$rootScope.testSpinner).toBeFalsy();
            });

            describe('return with the got promise', function () {

                beforeEach(function () {
                    test.injectFactory();
                });

                it('what never resolved', function () {
                    expect(test.CommonFactory.handlePromise(test.promise)).toBe(test.promise);
                });

                it('what resolved before used', function () {
                    test.deferred.resolve();
                    test.$rootScope.$apply();

                    expect(test.CommonFactory.handlePromise(test.promise)).toBe(test.promise);
                });

                it('what rejected before used', function () {
                    test.deferred.reject();
                    test.$rootScope.$apply();

                    expect(test.CommonFactory.handlePromise(test.promise)).toBe(test.promise);
                });

            });

            describe('check callbacks', function () {

                beforeEach(function () {
                    this.afterInjects.push(function () {
                        test.callbacks = {
                            'resolve': function () {
                            },
                            'reject': function () {
                            }
                        };
                        spyOn(test.callbacks, 'resolve');
                        spyOn(test.callbacks, 'reject');
                    });
                });

                it('resolved promise', function () {
                    test.injectFactory();

                    test.CommonFactory.handlePromise(test.promise, 'testSpinner',
                        test.callbacks.resolve, test.callbacks.reject);
                    expect(test.$rootScope.testSpinner).toBeTruthy();

                    test.deferred.resolve('foo');
                    test.$rootScope.$apply();

                    expect(test.$rootScope.testSpinner).toBeFalsy();
                    expect(test.callbacks.resolve).toHaveBeenCalledWith('foo');
                    expect(test.callbacks.reject).not.toHaveBeenCalled();

                    expect(test.mocks.$alert).not.toHaveBeenCalled();
                });

                it('rejected promise', function () {
                    test.injectFactory();

                    test.CommonFactory.handlePromise(test.promise, 'testSpinner',
                        test.callbacks.resolve, test.callbacks.reject);
                    expect(test.$rootScope.testSpinner).toBeTruthy();

                    test.deferred.reject('bar');
                    test.$rootScope.$apply();

                    expect(test.$rootScope.testSpinner).toBeFalsy();
                    expect(test.callbacks.resolve).not.toHaveBeenCalled();
                    expect(test.callbacks.reject).toHaveBeenCalledWith('bar');

                    expect(test.mocks.$alert).toHaveBeenCalled();
                });
            });
        });
    });
});
