# vaccine-api-test
Test API service for World Class Government APIs.
## Endpoint test
URL: https://wcg-apis.herokuapp.com
- /registration
- /registration?{citizen}
- /citizen
- /citizen/{citizen_id}
- /reservation
- /reservation?{vaccine_url}
- /reservation?citizen_id={citizen_id}
## Running Test
```
python -m unittest test_api.py
```
## More information
- [Homepage](https://wcg-apis.herokuapp.com/)
- [Swagger API Document](https://wcg-apis.herokuapp.com/api-doc/)
