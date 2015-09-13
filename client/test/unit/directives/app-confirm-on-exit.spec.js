'use strict';

describe('appConfirmOnExit', function () {
    var test;

    beforeEach(module('appDirectives', 'partials'));

    beforeEach(function () {
        test = this;

        var mocks = {
                '$modal': {
                    '$id': 'fooId'
                },
                '$window': {
                    'confirm': function () {
                        return test.confirmReply;
                    }
                },
                'gettextCatalog': {
                    'getString': function () {
                        return 'bar';
                    }
                }
            },

            injectDirective = function () {
                module(function ($provide) {
                    $provide.value('$window', mocks.$window);
                    $provide.value('gettextCatalog', mocks.gettextCatalog);
                });
                spyOn(mocks.$window, 'confirm').and.callThrough();
                spyOn(mocks.gettextCatalog, 'getString').and.callThrough();

                inject(function ($compile, $rootScope) {
                    test.$compile = $compile;
                    test.$rootScope = $rootScope;
                    test.$scope = $rootScope.$new();

                    test.container = helper.compileTemplate(test, '<form ' +
                        'name="testForm" ' +
                        'app-confirm-on-exit="testForm.$dirty" ' +
                        'app-modal-id="testModalId"></form>');
                });
            };

        this.mocks = mocks;
        this.injectDirective = injectDirective;
    });

    beforeEach(function () {
        test.injectDirective();

        test.confirmReply = true;
        test.$scope.testForm.$setPristine();
        test.$scope.testModalId = undefined;
        test.$scope.$apply();
    });

    describe('on close modal', function () {
        it('do nothing when there are not any dirty forms', function () {
            var event;

            event = test.$rootScope.$emit('modal.hide.before', test.mocks.$modal, null);
            expect(test.mocks.$window.confirm).not.toHaveBeenCalled();
            expect(event.defaultPrevented).toBeFalsy();
        });

        it('do nothing when there are not set app-modal-name', function () {
            var event;

            test.$scope.testForm.$setDirty();
            test.$scope.$apply();

            event = test.$rootScope.$emit('modal.hide.before', test.mocks.$modal, null);
            expect(test.mocks.$window.confirm).not.toHaveBeenCalled();
            expect(event.defaultPrevented).toBeFalsy();
        });

        it('left dirty forms when cancel on confirm', function () {
            var event;

            test.$scope.testModalId = 'fooId';
            test.$scope.$apply();
            test.$scope.testForm.$setDirty();
            test.confirmReply = false;

            event = test.$rootScope.$emit('modal.hide.before', test.mocks.$modal, null);
            expect(test.mocks.$window.confirm).toHaveBeenCalledWith('bar');
            expect(event.defaultPrevented).toBeTruthy();
        });

        it('close forms dirty forms when ok on confirm', function () {
            var event;

            test.$scope.testModalId = 'fooId';
            test.$scope.$apply();
            test.$scope.testForm.$setDirty();

            event = test.$rootScope.$emit('modal.hide.before', test.mocks.$modal, null);
            expect(test.mocks.$window.confirm).toHaveBeenCalledWith('bar');
            expect(event.defaultPrevented).toBeFalsy();
        });

    });

    describe('on change url', function () {
        it('do nothing when there are not any dirty forms', function () {
            var event;

            event = test.$rootScope.$emit('$locationChangeStart', null, null);
            expect(test.mocks.$window.confirm).not.toHaveBeenCalled();
            expect(event.defaultPrevented).toBeFalsy();
        });


        it('left dirty forms when cancel on confirm', function () {
            var event;
            test.$scope.testForm.$setDirty();
            test.confirmReply = false;

            event = test.$rootScope.$emit('$locationChangeStart', null, null);
            expect(test.mocks.$window.confirm).toHaveBeenCalledWith('bar');
            expect(event.defaultPrevented).toBeTruthy();
        });

        it('close forms dirty forms when ok on confirm', function () {
            var event;
            test.$scope.testForm.$setDirty();

            event = test.$rootScope.$emit('$locationChangeStart', null, null);
            expect(test.mocks.$window.confirm).toHaveBeenCalledWith('bar');
            expect(event.defaultPrevented).toBeFalsy();
        });
    });

    describe('on unload window', function () {
        it('do nothing when there are not any dirty forms', function () {
            var event;

            event = test.$rootScope.$emit('windowBeforeUnload', test.mocks.$modal, null);
            expect(test.mocks.$window.confirm).not.toHaveBeenCalled();
            expect(event.defaultPrevented).toBeFalsy();
        });

        it('confirm dirty forms closing', function () {
            var event;
            test.$scope.testForm.$setDirty();

            event = test.$rootScope.$emit('windowBeforeUnload', test.mocks.$modal, null);
            expect(event.defaultPrevented).toBeTruthy();
        });
    });
});
