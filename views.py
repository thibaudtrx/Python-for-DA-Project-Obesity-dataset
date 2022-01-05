from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
import os
import pickle

# Create your views here.
def index(request):
    template = loader.get_template('Visu/index.html')
    context = {"date":datetime.today()}
    return HttpResponse(template.render(context,request))

def predict(request):
    if request.method == 'POST':
        
        Gender = int(request.POST['Gender'])  
        Age = int(request.POST['Age'])
        Height = float(request.POST['Height'])
        Weight = float(request.POST['Weight'])
        family_history_with_overweight = int(request.POST['family_history_with_overweight'])
        Caloric_food = int(request.POST['Caloric_food'])
        Veggies = int(request.POST['Veggies'])
        Nb_meals = int(request.POST['Nb_meals'])
        Eat_between_meals = int(request.POST['Eat_between_meals'])
        Smoke = int(request.POST['Smoke'])
        Water = int(request.POST['Water'])
        Monitor_calories = int(request.POST['Monitor_calories'])
        Physical_activity = int(request.POST['Physical_activity'])
        Time_spent_on_tech = int(request.POST['Time_spent_on_tech'])
        Alcohol = int(request.POST['Alcohol'])
        
        Transport_means = int(request.POST['Transport_means'])
        temp_trans = [0 for i in range(0,4)]
        temp_trans[Transport_means]=1
        
        
        d = os.getcwd() #adress of the project
        filename = d+'/Visu/static/model/model.sav'
        

        loaded_model = pickle.load(open(filename, 'rb'))

        predicts=[Gender,Age,Height,Weight,family_history_with_overweight,
                  Caloric_food,Veggies,Nb_meals,Eat_between_meals,Smoke,Water,
                  Monitor_calories,Physical_activity,Time_spent_on_tech,Alcohol]
        predicts=predicts+temp_trans
        # Prediction on Test set
        y_pred = loaded_model.predict([predicts])       
        if (y_pred==0):
            y_pred="You have an Insufficient Weight. "
        elif(y_pred==1):
            y_pred="You have a Normal Weight."
        elif(y_pred==2):
            y_pred="You have a level 1 OverWeight."
        elif(y_pred==3):
            y_pred="You have a level 2 OverWeight."
        elif(y_pred==4):
            y_pred="You have an Obesity type 1."
        elif(y_pred==5):
            y_pred="You have an Obesity type 2."
        elif(y_pred==6):
            y_pred="You have an Obesity type 3."
        
            
        context = {"y_pred": y_pred}
        return render(request, "Visu/prediction.html", context)