# import Api response lib
from .helpers.response import Response

def handle_404_errors(e):
    return Response(message=f"{e}", status_code=404).send()

def handle_500_errors(e):
    return Response(message=f"{e}", status_code=500).send()
