#### import

# from myproduct.api import anything

#### read

def read(request):

    '''Basic echo test from README.md.'''

    response = request.copy()
    response.ok = True
    return response
