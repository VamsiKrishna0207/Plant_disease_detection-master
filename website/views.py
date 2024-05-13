from flask import Blueprint, render_template, request, flash, jsonify, Response
from flask_login import login_required, current_user
from .models import History
from . import db, load_image, check, output
import json
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/main', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html",user=current_user)



@views.route('/history')
def history():
    return render_template("history.html",values=History.query.all(),user=current_user)


@views.route('/more')
def more():
    return render_template("more.html",user=current_user)


@views.route('/morep')
def morep():
    return render_template("morep.html",user=current_user)


@views.route('/moren')
def moren():
    return render_template("moren.html",user=current_user)



@views.route('/', methods=['GET', 'POST'])
@login_required
def main():
    return render_template("Main.html",user=current_user)


@views.route('/contact')
def contact():
    return render_template("Contact.html",user=current_user)



@views.route('/about')
def about():
    return render_template("About.html",user=current_user)




@views.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        mim=f.mimetype
        j=f.read()
        full_pipeline = check()
        img = load_image(f)
        prediction = output(full_pipeline,img)
        sug=[["Suggestions to decrease <b>Potassium deficiency</b>:","Use potassium sulphate or potassium chloride. ","Use hardwood ashes.","Use granite dust.","Use feldspar and mica."],["Suggestions to decrease <b>Nitrogen deficiency</b>:","Use Nitrate or Ammonium based fertilizers. ","Use coffee grounds.","Use manure.","Use human urine.","Plant nitrogen fixing plants like clover, soybeans"],["Suggestions to decrease <b>Phosphorus deficiency</b>:","Use Phosphorus fertilizers like mushroom compost. ","Use bone meat.","Use rock phosphate.","Use animal dung.","Use fish emulsion or pig droppings","Do not over water the plants"]]
        act_sug=["Your plant is <b>Healthy</b>, please take care and <br> give right attention to your plant"]
        if prediction=="Potassium Deficiency":
            act_sug=sug[0]
        elif prediction=="Nitrogen Deficiency":
            act_sug=sug[1]
        elif prediction=="Phosphorus Deficiency":
            act_sug=sug[2]
        out=""
        for i in range(0,len(act_sug)):
            if i==0:
                out+=act_sug[i]
            else:
                out+="<li>"+act_sug[i]+"</li>"
        print(mim)
        filename = secure_filename(f.filename)
        hist=History(user_email=current_user.email,pre_date=func.now(),img=j,prediction=prediction,mimetype=mim)
        db.session.add(hist)
        db.session.commit()
        return [prediction,out]
    return None



