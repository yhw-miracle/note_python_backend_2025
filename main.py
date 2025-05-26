import sys
from server import app

if sys.platform == "linux":
    from gunicorn.app.base import BaseApplication

    class NoteServerApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()
        
        def load_config(self):
            config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)
        
        def load(self):
            return self.application


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        app.run(host="0.0.0.0", port=app.config["PORT"], debug=False, processes=True)
    else:
        NoteServerApplication(app, {"bind": f'0.0.0.0:{app.config["PORT"]}', "workers": app.config["WORKERS"]}).run()
