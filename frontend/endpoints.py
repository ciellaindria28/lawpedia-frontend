# change this to the url of the backend server
BASE_URL = 'http://localhost:8002'
BASE_AUTH_URL = 'http://localhost:8001'

# endpoints
REGISTER_URL = BASE_AUTH_URL + '/auth/register'
LOGIN_URL = BASE_AUTH_URL + '/auth/login'
LOGOUT_URL = BASE_AUTH_URL + '/auth/logout'

CREATE_PDF_URL = BASE_URL + '/download/orders'
GET_PDF_LIST = BASE_URL + '/download/get_pdf_list'
GET_PDF_RESULT_URL = BASE_URL + '/download/get_pdf_result'