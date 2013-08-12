from apiphant.background import seconds

def on_error(error):
    send_email_message(to=email_config['user'], subject='Error', text=error, **email_config)
    # See https://pypi.python.org/pypi/send_email_message

@seconds(60)
def update_something():
    pass
    # 1/0
