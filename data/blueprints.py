import flask


blueprint = flask.Blueprint('blueprints', __name__, template_folder='templates')


@blueprint.route('/')
def foo():
    return flask.jsonify(dict())
