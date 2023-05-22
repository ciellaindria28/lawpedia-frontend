# change this to the url of the backend server
BASE_URL = 'http://localhost:8002'
BASE_AUTH_URL = 'http://localhost:8001'
BASE_PRODUCT_URL = 'http://localhost:3000'

# endpoints
REGISTER_URL = BASE_AUTH_URL + '/auth/register'
LOGIN_URL = BASE_AUTH_URL + '/auth/login'
LOGOUT_URL = BASE_AUTH_URL + '/auth/logout'
USER_CHECK_URL = BASE_AUTH_URL + '/auth/user'

CREATE_PDF_URL = BASE_URL + '/download/orders'
GET_PDF_LIST = BASE_URL + '/download/get_pdf_list'
GET_PDF_RESULT_URL = BASE_URL + '/download/get_pdf_result'

CREATE_PRODUCT_URL = BASE_PRODUCT_URL + '/products/create'
UPDATE_PRODUCT_URL = BASE_PRODUCT_URL + '/products/update/:id'
GET_ALL_PRODUCT_URL = BASE_PRODUCT_URL + '/products/'
GET_PRODUCT_URL = BASE_PRODUCT_URL + '/products/:id'
DELETE_PRODUCT_URL = BASE_PRODUCT_URL + '/products/delete/:id'