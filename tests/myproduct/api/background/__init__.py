
#### on_error

def on_error(error):
    send_email_message(to=email_config['user'], subject='Error', text=error, **email_config) # See https://pypi.python.org/pypi/send_email_message

#### tasks

import myproduct.api.background.update_something
