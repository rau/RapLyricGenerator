from flask import Flask, render_template, request
import lyrics
import os

os.chdir(r'C:\Users\rauna\Documents\GitHub\RapLyricGenerator')
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        return render_template('home.html', title='Home!')
    else:
        return render_template('home.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    if(request.method == 'POST'):
        return render_template('about.html', ABP=lyrics.getLines())
    else:
        return render_template('about.html', ABP=lyrics.getLines())

if __name__ == "main":
    app.run(debug=True)
