from waitress import serve
from portal import portal

serve(portal, host='0.0.0.0', port=9000)
