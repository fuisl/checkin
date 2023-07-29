from flask import Flask, flash, redirect, render_template, request, url_for, Response
from helper import apology 
from flask_session import Session 
from camera import WebCam
import server

import os

#declare all collections
face_collection = server.UserFace()
user_collection = server.User()
ticket_collection = server.Ticket()
ticket_data_collection = server.TicketData()

# Update directory 
os.chdir(os.path.dirname(__file__)) 

# Configure application
app = Flask(__name__, template_folder="templates") 

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.update(SECRET_KEY=os.urandom(24))
app.config.from_object(__name__) 

def webcam(camera, id):
    image_path_list = [] #list to save images paths

    while True:
        frame, image_path = camera.gen_cam(user_id=id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        image_path_list.append(image_path)
        
        if camera.counter >= 40:
            del camera
            print('Done!')
            break
    
    #add paths to database
    face_collection.add_face(id=id, image_paths=image_path_list)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response 

@app.route("/", methods=["GET", "POST"])
def index(): 

    genders = ["Male", "Female", "Other"]
    ticket_classes_list = ["STANDARD", "VIP"] 

    # Branching on method
    if request.method == "POST": 

        # Check the perimeter 
        # Check full name 
        if not request.form.get("full_name"): 
            return apology("Must provide full name", 400) 
        
        # Check student ID
        if not request.form.get("student_id"): 
            return apology("Must provide student ID", 400) 
        
        if len(request.form.get("student_id")) != 8: 
            return apology("Invalid student ID", 400) 
        
        # Check gender 
        if not request.form.get("gender"): 
            return apology("Must select gender")
        
        if request.form.get("gender") not in genders: 
            return apology("Unvalid gender", 400)
        
        # Check email 
        if not request.form.get("email"): 
            return apology("Must provide email", 400)
        
        if not ("@" in request.form.get("email") and (request.form.get("email").endswith((".com", ".vn")))):
            return apology("Unvalid email", 400)
        
        # Check ticket class 
        if not request.form.get("ticket_class"): 
            return apology("Must select ticket class")
        
        if request.form.get("ticket_class") not in ticket_classes_list: 
            return apology("Unvalid ticket class", 400)
        
        # Check ticket num 
        if request.form.get("face") == "yes":
            ticket_num = 1
        else: 
            if (not request.form.get("ticket_num")):
                return apology("Must provide the number of tickets", 400)
            ticket_num = int(request.form.get("ticket_num"))
            
        name = request.form.get("full_name")
        student_id = request.form.get("student_id")
        gender = request.form.get("gender")
        email = request.form.get("email")
        ticket_class = request.form.get("ticket_class")

        #gather info
        user_info = {
            "_id": student_id,
            "name": name,
            "email": email,
            "gender": gender
        }

        #add user
        user_collection.add_user(user_info)

        #take a required amount of tickets
        tickets_bought = ticket_data_collection.buy_ticket(ticket_class=ticket_class, quantity=ticket_num)

        if tickets_bought != {}:
            print("Adding!")
            #add one by one to ticket collection
            for ticket in tickets_bought:
                print(ticket)
                ticket_id = ticket['_id']
                ticket_class = ticket['class']
                
                ticket_collection.add_ticket(
                    ticket_id=ticket_id,
                    ticket_class=ticket_class,
                    user_id=student_id
                )

        # Redirect 
        if request.form.get("face") == "yes": 

            return redirect(f"/camera/<{student_id}>")

        else: 
            return redirect("/view")

    else: 
        return render_template("home.html")

@app.route("/view", methods=["GET"])
def view(): 

    return render_template("view.html")

@app.route("/camera/<student_id>", methods=["GET"])
def camera(student_id): 

    return render_template("camera.html", student_id=student_id) 

@app.route('/video_feed/<id>')
def video_feed(id):
    video_stream = WebCam()

    return Response(webcam(video_stream, id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)