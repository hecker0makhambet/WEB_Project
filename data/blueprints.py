import flask


blueprint = flask.Blueprint('blueprints', __name__, template_folder='templates')


@blueprint.route('/blueprint')
def foo():
    return flask.jsonify(dict())
