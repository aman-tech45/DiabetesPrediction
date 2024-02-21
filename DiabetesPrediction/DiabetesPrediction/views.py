# views.py

from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def home(request):
    return render(request, 'home.html')

def predict(request):
    return render(request, 'predict.html')

def guide(request):
    return render(request, 'guide.html')

def result(request):
    # Load the dataset

    data = pd.read_csv("/Users/amanjha/Desktop/RBL/DiabetesPrediction/DiabetesPrediction/static/DiabetesPrediction/dataset/diabetees.csv")

    # Split the data into features (X) and target (Y)
    X = data.drop('Outcome', axis=1)
    Y = data['Outcome']

    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Create and train the random forest classifier model (use the parameters you prefer)
    model = RandomForestClassifier(n_estimators=100, random_state=42)  # You can adjust the hyperparameters
    model.fit(X_train, Y_train)

    # Get user input from the request
    try:
        val1 = float(request.GET.get('n1', 0.0))
        val2 = float(request.GET.get('n2', 0.0))
        val3 = float(request.GET.get('n3', 0.0))
        val4 = float(request.GET.get('n4', 0.0))
        val5 = float(request.GET.get('n5', 0.0))
        val6 = float(request.GET.get('n6', 0.0))
        val7 = float(request.GET.get('n7', 0.0))
        val8 = float(request.GET.get('n8', 0.0))
    except ValueError:
        # Handle the case where the conversion fails
        # You can set a default value or return an error response
        val1 = val2 = val3 = val4 = val5 = val6 = val7 = val8 = 0.0
        # Or you can raise an exception or return an error response
        # return HttpResponse("Invalid input, please provide valid numbers.")

    # Make predictions using the model
    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])

    # Determine the result based on the prediction
    if pred == 1:
        result1 = 'Positive'
    else:
        result1 = 'Negative'

    return render(request, 'predict.html', {"result2": result1})

# Additional part
from django.shortcuts import render  # Import your actual form

def predict_view(request):
    note_for_positive = ""  # Initialize the note
    result = ""  # Initialize result

    if request.method == 'POST':
        form = YourPredictionForm(request.POST)
        if form.is_valid():
            # Your existing prediction logic
            result = make_prediction(form.cleaned_data['n1'], form.cleaned_data['n2'], form.cleaned_data['n3'],
                                      form.cleaned_data['n4'], form.cleaned_data['n5'], form.cleaned_data['n6'],
                                      form.cleaned_data['n7'], form.cleaned_data['n8'])

            # Check if the result is positive and set the note_for_positive
            if result == 'positive':
                note_for_positive = "You have tested positive. Please follow these guidelines..."

    else:
        form = YourPredictionForm()

    return render(request, 'predict_page.html', {'form': form, 'result': result, 'note_for_positive': note_for_positive})
