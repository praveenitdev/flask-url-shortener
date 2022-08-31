from flask import Flask,render_template,request,url_for,flash,redirect,abort
import json,os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=["GET","POST"])
def home():
    urls = {}
    if request.method == 'GET':
        return render_template("index.html",name="praveen")
    else:
        # Validate duplicate short names
        if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)

        if request.form["code"] in urls.keys():
            flash(f'Short Name already taken..{urls}',"danger")
            return redirect("/")
        elif 'url' in request.form.keys():
            # Store the post data into a urls dict
            urls[request.form["code"]] = {"url":request.form["url"]}
        else:
            f = request.files['file']
            file_name = secure_filename(str(f.filename))
            full_name =f'{request.form["code"]}_{file_name}'
            f.save("static/user_files/"+full_name)
            urls[request.form["code"]] = {"file":full_name}

        
        # Save the urls dict into a json file
        with open("urls.json","w") as url_file:
            json.dump(urls,url_file)
        flash(f'Your Shortener url successfully created.. {urls}',"success")
        return redirect("/")
    
@app.route("/<string:code>")
def url_redirect(code):
    urls = {}
    if os.path.exists("urls.json"):
            with open("urls.json") as urls_file:
                urls = json.load(urls_file)
                if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]["url"])
                    else:
                        return redirect(url_for('static',filename='user_files/'+urls[code]["file"]))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
