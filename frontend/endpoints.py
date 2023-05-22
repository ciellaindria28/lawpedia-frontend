# change this to the url of the backend server
BASE_URL = "https://lawpedia-frontend-i6pjjcb5oq-et.a.run.app"
BASE_AUTH_URL = "https://lawpedia-product-i6pjjcb5oq-et.a.run.app"
BASE_PRODUCT_URL = "https://lawpedia-product-i6pjjcb5oq-et.a.run.app"
BASE_CART_ORDER_URL = "https://lawpedia-i6pjjcb5oq-et.a.run.app"

# auth endpoints
REGISTER_URL = BASE_AUTH_URL + "/auth/register"
LOGIN_URL = BASE_AUTH_URL + "/auth/login"
LOGOUT_URL = BASE_AUTH_URL + "/auth/logout"
USER_CHECK_URL = BASE_AUTH_URL + "/auth/user"

# download endpoints
CREATE_PDF_URL = BASE_URL + "/download/orders"
GET_PDF_LIST = BASE_URL + "/download/get_pdf_list"
GET_PDF_RESULT_URL = BASE_URL + "/download/get_pdf_result"

CREATE_PRODUCT_URL = BASE_PRODUCT_URL + "/products/create"
UPDATE_PRODUCT_URL = BASE_PRODUCT_URL + "/products/update/:id"
GET_ALL_PRODUCT_URL = BASE_PRODUCT_URL + "/products/"
GET_PRODUCT_URL = BASE_PRODUCT_URL + "/products/:id"
DELETE_PRODUCT_URL = BASE_PRODUCT_URL + "/products/delete/:id"
# cart endpoints
CART_URL = BASE_CART_ORDER_URL + "/cart"
CART_BY_ID_URL = BASE_CART_ORDER_URL + "/cart/<int:order_id>"
ADD_PRODUCT_URL = BASE_CART_ORDER_URL + "/cart/add"
UPDATE_QUANTITY_URL = BASE_CART_ORDER_URL + "/cart/update-quantity"
DELETE_CART_URL = BASE_CART_ORDER_URL + "/cart/delete"

# order endpoints
ORDER_URL = BASE_CART_ORDER_URL + "/orders"
ORDER_BY_ID_URL = BASE_CART_ORDER_URL + "/orders/<int:order_id>"
UPDATE_ORDER_STATUS_URL = BASE_CART_ORDER_URL + "/orders/updateStatus"
CONFIRM_DELIVERY_URL = BASE_CART_ORDER_URL + "/orders/confirmDelivery"
CHECKOUT_ORDER_URL = BASE_CART_ORDER_URL + "/orders/checkout"
