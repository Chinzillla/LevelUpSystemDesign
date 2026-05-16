def register_routes(app, *blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)