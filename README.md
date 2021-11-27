# vaccine-api-test
[![Build Status](https://app.travis-ci.com/sujinunt/vaccine-api-test.svg?branch=main)](https://app.travis-ci.com/sujinunt/vaccine-api-test)

Test API service for World Class Government APIs.
## Endpoint test
URL: https://wcg-apis.herokuapp.com
- /registration
- /registration?{citizen}
- /registration/{citizen_id}
- /reservation
- /reservation?{vaccine_url}
- /reservation/{citizen_id}
- /database/citizen
- /database/reservation
## Install Python module
```
pip install -r requirements.txt
```
## Running Test
```
python -m unittest test_api.py
```
## More information
- [Homepage](https://wcg-apis.herokuapp.com/)
- [Swagger API Document](https://wcg-apis.herokuapp.com/api-doc/)
