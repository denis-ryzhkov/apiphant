# from myproduct.api import anything
def read(request):
    response = request.copy()
    response.ok = True
    return response
