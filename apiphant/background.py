
#### import

from adict import adict

#### tasks

tasks = []

#### seconds

def seconds(number_of_seconds):
    def decorated_task(task):
        tasks.append(adict(
            task=task,
            seconds=number_of_seconds,
            last=0,
            name=task.__name__,
        ))
        return task
    return decorated_task

#### main

def main():

    #### become cooperative

    import gevent.monkey
    gevent.monkey.patch_all()

    #### import

    from apiphant.paths import init_paths
    from gevent import sleep
    import logging, sys, time
    from traceback import format_exc

    #### command-line config

    usage = 'Usage: apiphant-background path/to/myproduct'

    try:
        _, product_path = sys.argv

    except ValueError:
        exit(usage)

    #### paths

    api_path, product_name = init_paths(product_path)

    #### logging

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s at %(module)s.%(funcName)s:%(lineno)d [%(asctime)s] %(message)s') # To sys.stderr by default.

    #### import myproduct.api.background to init tasks[] with @seconds

    product_module_name = '{product_name}.api.background'.format(product_name=product_name)
    product_module = __import__(product_module_name, globals(), locals())
    on_error = getattr(product_module.api.background, 'on_error', None)

    #### loop

    logging.info('\nApiphant is scheduling {product_module_name}\n'.format(product_module_name=product_module_name))

    while True:

        #### Select tasks ready to run.

        now = time.time()

        ready_tasks = [
            task
            for task in tasks
            if now - task.last >= task.seconds
        ]

        #### Sort to respect desired "seconds" as possible with non-overlapping mode.

        ready_tasks.sort(key=lambda task: task.seconds)

        #### Run them one by one, non-overlapping, safe, logging.

        for task in ready_tasks:
            task.last = now # Even if it fails, we don't want to retry before the next time it should run.

            try:
                task.task()

            except:
                error = 'Task {task} failed:\n{traceback}'.format(task=task.name, traceback=format_exc())
                logging.error(error)

                #### on_error
 
                if on_error: # E.g. send_email_message(to=email_config['user'], subject='Error', text=error, **email_config)
                    try:
                        on_error(error)
 
                    except:
                        logging.error('on_error failed:\n{traceback}'.format(traceback=format_exc()))

                    else:
                        logging.info('on_error: OK.')

            else:
                logging.info('Task {task}: OK.'.format(task=task.name))

        #### Minimal 1-second sleep to not make the loop too tight.

        sleep(1)
