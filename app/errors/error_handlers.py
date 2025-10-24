from flask import flash, redirect, request, url_for
from werkzeug.exceptions import (
    HTTPException,
    BadRequest,            # 400
    Unauthorized,          # 401
    Forbidden,             # 403
    NotFound,              # 404
    Conflict,              # 409
    PreconditionFailed,    # 412
    ServiceUnavailable,    # 503
    GatewayTimeout,        # 504
    InternalServerError,   # 500
)


def _back():
    return redirect(request.referrer or url_for('auth.menu_page'))


def register_error_handlers(app):

    @app.errorhandler(400)
    def handle_400(e):
        flash("ERROR: Invalid request.", category="danger")
        return _back()

    @app.errorhandler(401)
    def handle_401(e):
        flash("ERROR: Unauthorized.", category="danger")
        return _back()

    @app.errorhandler(403)
    def handle_403(e):
        flash("ERROR: Forbidden.", category="danger")
        return _back()

    @app.errorhandler(409)
    def handle_409(e):
        flash("ERROR: Conflict detected.", category="danger")
        return _back()

    @app.errorhandler(412)
    def handle_412(e):
        flash("ERROR: Precondition failed.", category="danger")
        return _back()

    @app.errorhandler(503)
    @app.errorhandler(504)
    def handle_503_504(e):
        flash("ERROR: Service unavailable.", category="danger")
        return _back()

    @app.errorhandler(500)
    def handle_500(e):
        flash("ERROR: Internal server error.", category="danger")
        return _back()

  