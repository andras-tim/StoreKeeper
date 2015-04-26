angular.module('gettext').run(['gettextCatalog', function (gettextCatalog) {
/* jshint -W100 */
    gettextCatalog.setStrings('hu', {"Error {{status}}":"Hiba {{status}}","LogOut":"Kijelentkezés","Login":"Bejelentkezés","Main":"Főoldal","Password":"Jelszó","Sign in":"Bejelentkezés","The user's password is required":"A jelszót kötelező megadni","The user's username is required":"A felhasználónevet kötelező megadni","Username":"Felhasználónév","Welcome {{session.username}}!":"Üdvözöllek {{session.username}}!"});
/* jshint +W100 */
}]);