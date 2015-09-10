'use strict';

describe('Login view', function () {

    var elements = {};

    beforeEach(function () {
        browser.get('storekeeper/index.html#/login');

        elements.username = element(by.id('usernameInput'));
        elements.password = element(by.id('passwordInput'));
        elements.remember = element(by.id('rememberCheckbox'));
        elements.login = element(by.id('login'));
    });


    it('can not login with missing credentials', function () {
        elements.username.sendKeys('admin');
        elements.login.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url).toBe('/login');
        });
    });


    it('can not login without missing username', function () {
        elements.password.sendKeys('admin');
        elements.login.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url).toBe('/login');
        });
    });


    it('can not login without missing password', function () {
        elements.username.sendKeys('admin');
        elements.login.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url).toBe('/login');
        });
    });


    it('can login with valid credentials', function () {
        elements.username.sendKeys('admin');
        elements.password.sendKeys('admin');
        elements.login.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url).toBe('/items');
        });
    });

    it('can login with remember me', function () {
        elements.username.sendKeys('admin');
        elements.password.sendKeys('admin');
        elements.remember.click();

        expect(elements.remember.isSelected()).toBe(true);

        elements.login.click();

        browser.getLocationAbsUrl().then(function (url) {
            expect(url).toBe('/items');
        });
    });

});
