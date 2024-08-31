from flask import Flask, render_template, request
import joblib,sqlite3

app = Flask(__name__)

# Load the model
model = joblib.load("./models/randomforest.lb")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/planes')
def planes():
    return render_template('planes.html')

@app.route('/data_form')
def data_form():
    return render_template('data_form.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/data', methods=["POST"])
def data():
    if request.method == "POST":
        try:
            # Retrieve form data with default values
            gender = request.form.get("gender", type=int, default=0)
            customerType = request.form.get("customerType", type=int, default=0)
            typeOfTravel = request.form.get("typeOfTravel", type=int, default=0)
            
            age = request.form.get("age", type=int, default=0)
            flightDistance = request.form.get("flightDistance", type=int, default=0)
            inflightEntertainment = request.form.get("inflightEntertainment", type=int, default=0)
            baggageHandling = request.form.get("baggageHandling", type=int, default=0)
            cleanliness = request.form.get("cleanliness", type=int, default=0)
            departureDelay = request.form.get("departureDelay", type=int, default=0)
            arrivalDelay = request.form.get("arrivalDelay", type=int, default=0)
            classOfTravel = request.form.get("class")

            economy=0
            economy_plus=0
            if classOfTravel=="Economy":
                economy=1
            elif classOfTravel=="Economy Plus":
                economy_plus=1

            # Prepare data for prediction
            data_for_predict = [[
                age, flightDistance, inflightEntertainment, baggageHandling, cleanliness,
                departureDelay, arrivalDelay, gender,
                customerType, typeOfTravel,economy, economy_plus
            ]]

            # Predict satisfaction
            satisfaction_prediction = model.predict(data_for_predict)[0]

            # Print prediction for debugging
            print(f"Prediction: {satisfaction_prediction}")

            # Convert numerical labels to descriptive labels
            gender = "Male" if gender == 1 else "Female"
            customerType = "Loyal Customer" if customerType == 1 else "Disloyal Customer"
            typeOfTravel = "Business Travel" if typeOfTravel == 1 else "Personal Travel"
            result = "satisfied" if satisfaction_prediction == 1 else "Unsatisfied"

            query_to_insert = """
            Insert into planeDetails values(?,?,?,?,?,?,?,?,?,?,?,?)
            """
            conn  =  sqlite3.connect('planedata.db')
            cur = conn.cursor() 
            data  = (gender,customerType,typeOfTravel,age,flightDistance,inflightEntertainment,baggageHandling,cleanliness,
                            departureDelay,arrivalDelay,classOfTravel,result)
            cur.execute(query_to_insert, data)
            conn.commit() 
            print("Your record has been stored in database")
            cur.close() 
            conn.close()



            # Render appropriate page based on prediction
            if satisfaction_prediction == 0:
                return render_template('unsatisfied_page.html',
                                       gender=gender, customerType=customerType,
                                       typeOfTravel=typeOfTravel, classOfTravel=classOfTravel,
                                       age=age, flightDistance=flightDistance,
                                       inflightEntertainment=inflightEntertainment,
                                       baggageHandling=baggageHandling,
                                       cleanliness=cleanliness,
                                       departureDelay=departureDelay,
                                       arrivalDelay=arrivalDelay)
            else:
                return render_template('satisfied_page.html',
                                       gender=gender, customerType=customerType,
                                       typeOfTravel=typeOfTravel, classOfTravel=classOfTravel,
                                       age=age, flightDistance=flightDistance,
                                       inflightEntertainment=inflightEntertainment,
                                       baggageHandling=baggageHandling,
                                       cleanliness=cleanliness,
                                       departureDelay=departureDelay,
                                       arrivalDelay=arrivalDelay)

        except Exception as e:
            return f"An error occurred: {e}"
        
        

if __name__ == '__main__':
    app.run(debug=True)
