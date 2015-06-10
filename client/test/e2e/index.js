'use strict';

describe('StoreKeeper app', function () {

    it('should redirect index.html to index.html#/login when user was not authenticated', function () {
        browser.get('storekeeper/index.html');
        browser.getLocationAbsUrl().then(function (url) {
            expect(url.split('#')[1]).toBe('/login');
        });
    });

});
