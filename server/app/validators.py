from wtforms.validators import Email, Regexp


email = Email()

username = Regexp("^([a-z0-9][a-z0-9._-]?)*[a-z0-9]$")
