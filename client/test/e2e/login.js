'use strict';

describe('Login view', function() {

    beforeEach(function() {
      browser.get('storekeeper/index.html#/login');
    });


    it('can not login with missing credentials', function() {
        var username = element(by.model('user.username'));
        var password = element(by.model('user.password'));
        var sign_in = element(by.id('sign_in'));

        username.sendKeys('admin');
        sign_in.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url.split('#')[1]).toBe('/login');
        });
    });


    it('can not login without missing username', function() {
        var password = element(by.model('user.password'));
        var sign_in = element(by.id('sign_in'));

        password.sendKeys('admin');
        sign_in.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url.split('#')[1]).toBe('/login');
        });
    });


    it('can not login without missing password', function() {
        var username = element(by.model('user.username'));
        var sign_in = element(by.id('sign_in'));

        username.sendKeys('admin');
        sign_in.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url.split('#')[1]).toBe('/login');
        });
    });


    it('can login with valid credentials', function() {
        var username = element(by.model('user.username'));
        var password = element(by.model('user.password'));
        var sign_in = element(by.id('sign_in'));

        username.sendKeys('admin');
        password.sendKeys('admin');
        sign_in.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url.split('#')[1]).toBe('/main');
        });
    });

});
