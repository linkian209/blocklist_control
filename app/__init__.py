import datetime
import os
from flask import Flask, jsonify, request, redirect

def create_app():
    app = Flask(__name__)

    @app.route("/<deviceName>/", methods=["GET", "POST"])
    def action(deviceName):
        retval = {
            'timestamp': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'command': deviceName
        }

        if(deviceName != 'monstermash'):
            if(deviceName == 'block'):
                scriptname = os.path.join(app.root_path, 'scr/blockdomains.sh')
                retval['status'] = 'error' if os.system(scriptname) else 'ok'
            elif(deviceName == 'unblock'):
                scriptname = os.path.join(app.root_path, 'scr/unblockdomains.sh')
                retval['status'] = 'error' if os.system(scriptname) else 'ok'
            else:
                retval['status'] = 'unknown'
        else:
            retval['status'] = 'doing the monster mash'

        return jsonify(retval)

    @app.route("/edit", methods=["GET", "POST"])
    def edit():
        if(request.method == "GET"):
            data = ''

            # Check if the domain list exists
            if(os.path.exists(os.path.join(app.root_path, 'scr/domains'))):
                with open(os.path.join(app.root_path, 'scr/domains'), 'r') as f:
                    data = f.read().replace('\\\\', '\\')
            
            # Return response
            return '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Domain List Editor</title>
                </head>
                <body>
                    <h1>Domain Control List</h1>
                    <form action="/edit" method="POST">
                        <textarea name="domains">{}</textarea>
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
            '''.format(data if data != '' else '')
        else:
            data = request.form['domains'].strip().replace('\r','').replace('\\','\\\\')

            # Write domains
            with open(os.path.join(app.root_path, 'scr/domains'), 'w') as f:
                f.write('{}\n'.format(data))

            return '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Domain List Editor</title>
                </head>
                <body>
                    <h1>Domain Control List</h1>
                    <form action="/edit" method="POST">
                        <textarea name="domains">{}</textarea>
                        <input type="submit" value="Submit">
                    </form>
                </body>
            </html>
            '''.format(request.form['domains'].strip())

    return app