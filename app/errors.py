"""Consistent JSON error responses."""

from werkzeug.exceptions import HTTPException


def error_response(message, status_code, details=None):
    payload = {"error": {"message": message, "status": status_code}}
    if details:
        payload["error"]["details"] = details
    return payload, status_code


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return error_response(error.description, error.code)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        app.logger.exception("Unhandled exception: %s", error)
        return error_response("An unexpected server error occurred.", 500)
