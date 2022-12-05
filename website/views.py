from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from website.models import Note, User, tasks
import json


views=Blueprint('views',__name__)



@views.route('/',methods=['GET','POST'])
@login_required
def home():
    notes=Note.query.order_by(Note.data).all()

    usernames= User.query.order_by(User.name).all()

    return render_template("home.html", user=current_user, notes=notes, usernames=usernames)





@views.route('/add', methods=['GET','POST'])
@login_required
def add():

    #get username for html loop
    usernames= User.query.order_by(User.name).all()
    list_dailytasks=Note.query.filter_by(dailytask=True).all()
    
    if request.method =='POST':

        #get data from html
        note=request.form.get('note')
        html_user=request.form.get('foruser')
        daily=request.form.get('dailytask')
        duration=request.form.get('duration')
        
        if len(note) <1:
            flash('Note is too short!',category='error')
            
        elif html_user=="both":
            if daily=="yes":

                new_note=Note(data=note, dailytask=True,duration=duration)
                for user in usernames:
                    user.notes.append(new_note)
                    db.session.add(new_note)
                    db.session.commit() 

                flash('Note added!', category='success')

 
            elif daily == "no":
                    
                new_note=Note(data=note, dailytask=False, duration=duration)
                for user in usernames:
                    user.notes.append(new_note)
                    db.session.add(new_note)
                    db.session.commit() 
                db.session.add(new_note)
                db.session.commit() 


                flash('Note added!', category='success')
 

        elif daily == "yes":
            get_user=User.query.filter_by(name=html_user).first()

            #add a note to db
            new_note=Note(data=note, dailytask=True,duration=duration)
            get_user.notes.append(new_note)
            db.session.add(new_note)
            db.session.commit()


            flash('Note added!', category='success')
 
        elif daily=="no":
            get_user=User.query.filter_by(name=html_user).first()

            #add note to db
            new_note=Note(data=note, dailytask=False,duration=duration)
            get_user.notes.append(new_note)
            db.session.add(new_note)
            db.session.commit()
            
            flash('Note added!', category='success')
 
        else:
            # this one could be improved
            flash('Somethin went wrong!', category='error')

    return render_template("add.html", user=current_user, list_dailytasks=list_dailytasks, usernames=usernames)



@views.route('/dailytasks',methods=['GET','POST'])
@login_required
def dailytasks():
    duration=Note.query.order_by(Note.duration).all()
    notes=Note.query.order_by(Note.data).all()
    usernames= User.query.order_by(User.name).all()


    if request.method == 'POST':

        #get data from html
        note=request.form.get('note')
        html_user=request.form.get('foruser')

        if len(note) <1:
            flash('Note is too short!',category='error')
            
        elif html_user == "both":

            new_note=Note(data=note, dailytask=True, duration=duration)
            for user in usernames:
                user.notes.append(new_note)
                db.session.add(new_note)
                db.session.commit() 

            flash('Note added!', category='success')


        elif html_user != "both":
            get_user=User.query.filter_by(name=html_user).first()

            new_note=Note(data=note, dailytask=True,duration=duration)
            get_user.notes.append(new_note)
            db.session.add(new_note)
            db.session.commit()


            flash('Note added!', category='success')

        else:
            # this one could be improved
            flash('Somethin went wrong!', category='error')

    return render_template("dailytasks.html", user=current_user, notes=notes, usernames=usernames)


@views.route('/usertasks', methods=['GET','POST'])
@login_required
def usertasks():

    #get username for html loop
    list_dailytasks=Note.query.filter_by(dailytask=True).all()
    notes=Note.query.order_by(Note.data).all()
    duration=Note.query.order_by(Note.duration).all()
       
    if request.method=='POST':

        #get data from html
        note=request.form.get('note')
        html_user=current_user
        daily=request.form.get('dailytask')
        
        if len(note) <1:
            flash('Note is too short!',category='error')
       
        elif daily=="yes":

            #add a note to db
            new_note=Note(data=note, dailytask=True,duration=duration)
            html_user.notes.append(new_note)
            db.session.add(new_note)
            db.session.commit()


            flash('Note added!', category='success')
 
        elif daily=="no":

            #add note to db
            new_note=Note(data=note, dailytask=False,duration=duration)
            html_user.notes.append(new_note)
            db.session.add(new_note)
            db.session.commit()
            
            flash('Note added!', category='success')
 
        else:
            # this one could be improved
            flash('Somethin went wrong!', category='error')

    return render_template("usertasks.html", user=current_user,notes=notes, list_dailytasks=list_dailytasks )



@views.route('/delete-note', methods=["POST"])
def delete_note():
    note=json.loads(request.data)
    noteId = note['noteId']
    note= Note.query.get(noteId)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({})



@views.route('/update_status/<int:id>', methods=["GET","POST"])
@login_required
def updateStatus(id):

    #need it for returning home page
    notes=Note.query.order_by(Note.data).all()
    usernames= User.query.order_by(User.name).all()

    note_to_update=Note.query.filter_by(id=id).first()
    if request.method=="POST":
        if note_to_update.finish == False:
            note_to_update.finish = True
            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template("home.html",user=current_user, notes=notes, usernames=usernames)
            except:
                flash("Error!")
                return render_template("update_status.html",user=current_user)
        else:
            note_to_update.finish = False
            try:
                db.session.commit()
                flash("User Updated Successfully!")
                return render_template("home.html",user=current_user, notes=notes, usernames=usernames)
            except:
                flash("Error!")
                return render_template("update_status.html", user=current_user)
    else:
        return render_template("update_status.html", user=current_user)