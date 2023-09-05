## Abstract
The objective of the project is to develop and deploy a Machine Learning based prediction microservice to classify if a student is proud of the Luddy School. The dataset consists of responses from several students in various courses at Luddy School to questions that analyze their sense of belonging to and involvement in their department.

## Installation Guidance
To run the project locally, use the following commands on the terminal
```bash
$ git clone git@github.com:samardeep331/Happy-Hoosiers.git
$ cd code
$ pip install -r requirements.txt
$ FLASK_APP=app.py flask run --host=0.0.0.0 -p 5001
```
This will allow the user to run the app on port 5001

If the user has docker installed locally, then the user can directly use the following command to run the app

```bash
$ docker run -p 5001:5000 samgurud/e534:latest     
```

Here 'samgurud/e534:latest' image will be downloaded from dockerhub which will be used to run the app.

## API Description
Below is the list of API endpoints that were developed for this project:

i.	Predict:
  1.	URI: http://149.165.154.170:5001/predict
  2.	Method: GET 
  3.	Content-type : text/html, charset=utf-8
  4.	Response(Server-side rendering): An HTML markup containing questions that are required for predicting the target variable value
 
ii.	Predict
  1.	URI: http://149.165.154.170:5001/predict
  2.	Method: POST
  3.	Payload: 'q1=Yes&q2=Computer+Science&q3=Strongly+Disagree&q4=Strongly+Disagree&q5=Strongly+Disagree&q6=Strongly+Disagree&q7=Strongly+Disagree&q8=Strongly+Disagree&q9=Strongly+Disagree&q10=Strongly+Disagree&q11=Strongly+Disagree&q12=Strongly+Disagree&q13=Strongly+Disagree&q14=Strongly+Disagree&q15=Strongly+Disagree&q16=Strongly+Disagree&q17=Strongly+Disagree&q18=this+is+my+first+year&q19=Yes&q20=Yes&q21=Yes&q22=Yes&q23=Yes&q24=Yes&q25=Female&q26=White+or+Caucasian&q27=Yes'
  4.	Content-Type: ‘application/x-www-form-urlencoded'Yes&q2=
  5.	Response : The response is a HTML markup which contains the prediction as well as the graph of features that is used to make the prediction.
		
iii.	Add Data: 
  1.	URI: http://149.165.154.170:5001/add_data
  2.	Method: GET	
  3.	Content-type : text/html, charset=utf-8
  4.	Response(Server-side rendering): An HTML markup containing questions that correspond to the features in the data set.

iv.	Add Data : 
  1.	URI: http://149.165.154.170:5001/add_data 
  2.	Method: POST
  3.	Content-type: ‘application/x-www-form-urlencoded'Yes 
  4.	Payload: 'q1=Yes&q2=Computer+Science&q3=Strongly+Disagree&q4=Strongly+Disagree&q5=Strongly+Disagree&q6=Strongly+Disagree&q7=Strongly+Disagree&q8=Strongly+Disagree&q9=Strongly+Disagree&q10=Strongly+Disagree&q11=Strongly+Disagree&q12=Strongly+Disagree&q13=Strongly+Disagree&q14=Strongly+Disagree&q15=Strongly+Disagree&q16=Strongly+Disagree&q17=Strongly+Disagree&q18=Strongly+Disagree&q19=this+is+my+first+year&q20=Yes&q21=Yes&q22=Yes&q23=Yes&q24=Yes&q25=Yes&q26=Female&q27=White+or+Caucasian&q28=Yes' 
  5.	Response: The response is a HTML markup which tells the user if the data has been added to the flat file storage. 


v.	Get Data : 
  1.	URI: http://149.165.154.170:5001/form_page 
  2.	Method: GET
  3.	Content-type: text/html, charset=utf-8
  4.	Response(Server-side rendering): An HTML markup that asks the user about the data that needs to be retrieved 

vi.	Get Data:
  1.	URI: http://149.165.154.270:5001/form_page 
  2.	Method: POST	
  3.	Payload: 'q1=1&q2=1&q3=Luddy+or+not%3F&q3=luddy_department+&q3=sense+of+belonging+_1&q3=sense+of+belonging+_2' 
  4.	Content-type: ‘application/x-www-form-urlencoded’e&q3=Strongl
  5.	Response: The response is a HTML markup containing a table which contains the data that the user requested.

