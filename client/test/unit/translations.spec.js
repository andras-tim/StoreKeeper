'use strict';

describe('translations', function () {
    var test,
        externalLanguages;

    beforeEach(module('gettext'));

    beforeEach(function () {
        test = this;

        var mocks = {
                'gettextCatalog': {
                    'setLanguages': [],
                    'setStrings': function (language) {
                        this.setLanguages.push(language);
                    }
                }
            },

            injectModule = function () {
                module(function ($provide) {
                    $provide.value('gettextCatalog', mocks.gettextCatalog);
                });
                spyOn(mocks.gettextCatalog, 'setStrings').and.callThrough();

                // inject() calls run() and config() directives
                inject();
            };

        this.mocks = mocks;
        this.injectModule = injectModule;
    });

    beforeEach(function () {
        externalLanguages = [
            'hu'
        ];
    });

    it('is contains all external languages', function () {
        test.mocks.gettextCatalog.setLanguages = [];
        test.injectModule();

        expect(test.mocks.gettextCatalog.setStrings).toHaveBeenCalled();
        expect(test.mocks.gettextCatalog.setLanguages).toEqual(externalLanguages);
    });
});
