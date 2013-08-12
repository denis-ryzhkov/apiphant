
from adict import adict
import os, sys

def init_paths(product_path):

    product_path = os.path.abspath(product_path) # /absolutized/path/to/myproduct

    api_path = os.path.join(product_path, 'api') # /absolutized/path/to/myproduct/api
    if not os.path.isdir(api_path):
        exit('Dir not found: {api_path}'.format(api_path=api_path))

    product_parent_path, product_name = os.path.split(product_path.rstrip(os.sep)) # /absolutized/path/to, myproduct
    sys.path.insert(0, product_parent_path) # Now it is possible: from myproduct.api import anything

    return api_path, product_name
