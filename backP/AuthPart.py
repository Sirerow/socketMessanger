from flask import Blueprint, render_template, redirect,request
from flask_login import login_user
from werkzeug.security import check_password_hash
from DBase import DB
from backP.UserLogin import UserLogin

auth_bp=Blueprint("auth", __name__)


@auth_bp.route('/')
@auth_bp.route('/authorization', methods=["GET","POST"])
def auth():
    if request.method=="POST":
        form=request.form
        print(form)
        print(form["login"])
        userKeyData=DB().getUserOnLogin(form["login"])
        if userKeyData!=None:
            if userKeyData[0]==form["login"] and check_password_hash(form["password"],userKeyData[2]):
                LM = UserLogin().createUser(DB().getUserOnLogin(form["login"]))
                login_user(LM)
            if userKeyData[0] == form["login"] and not check_password_hash(form["password"], userKeyData[2]):
                return redirect("/authorization")
        else:
            DB().addUser(form["login"], form["password"])
            LM = UserLogin().createUser(DB().getUserOnLogin(form["login"]))
            login_user(LM)
        return redirect("/chat")
    else:
        return render_template("authorization.html")
