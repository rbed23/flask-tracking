from flask import current_app, Markup, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException


def error_handler(error):
    current_app.logger.warning(
        f"Request resulted in {error}", exc_info=True)

    if isinstance(error, HTTPException):
        description = error.get_description(request.environ)
        code = error.code
        name = error.name
    else:
        description = ("We encountered an error "
                       "while trying to fulfill your request")
        code = 500
        name = 'Internal Server Error'

    templates_to_try = ['errors/{}.html'.format(code),
                        'errors/generic.html']
    return render_template(templates_to_try,
                           code=code,
                           name=Markup(name),
                           description=Markup(description),
                           error=error)


def init_app(app):
    for exception in default_exceptions:
        app.register_error_handler(exception, error_handler)

    app.register_error_handler(Exception, error_handler)