from flask.ext import restful


class RestfulApiWithoutSimpleAuth(restful.Api):
    def unauthorized(self, response):
        """ Given a response, change it to ask for credentials """

        allow_simple_auth = self.app.config.get("ALLOW_API_SIMPLE_AUTH", False)
        if allow_simple_auth:
            realm = self.app.config.get("HTTP_BASIC_AUTH_REALM", "flask-restful")
            response.headers['WWW-Authenticate'] = "Basic realm=\"%s\"" % realm

        return response
