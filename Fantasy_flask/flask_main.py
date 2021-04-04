from flask import Flask,url_for,render_template,redirect,request
from form import CricketForm
from calc_score import Get_text,openfile

app = Flask(__name__)

app.config['SECRET_KEY'] = '3d8474dad295984daff08183be0825d9'

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    form = CricketForm()
    if form.validate_on_submit():
        f = Get_text(form.url.data,form.innings.data)
        text = openfile(f,form.innings.data)
        return render_template('result.html',text=text)
    return render_template('home.html',form=form)


@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)