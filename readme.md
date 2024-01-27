# Govee night light

* Python lambda function deployed to AWS
* Event triggers from a cron schedule every 30 minutes
* Changes color of the light bulb :bulb: depending on the time of day
* Used to communicate to my daughters when it is ok to wake up :sunrise:




### Deploy Python Lambda functions with .zip file [aws doc here](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
```
pip install -r requirements.txt --target ./package requests

cd package

zip -r ../manage-light-deployment-package.zip . 

cd ..

zip -g  manage-light-deployment-package.zip manage_light_function.py get_time.py colors.py

aws lambda update-function-code --function-name manageLight --zip-file fileb://manage-light-deployment-package.zip
```



### Test locally

`` 
python-lambda-local manage_light_function.py -f lambda_handler event.json
``
