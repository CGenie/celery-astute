from __future__ import absolute_import

import celery
import time

from proj.celery import app


class BaseTask(celery.Task):
    abstract = True
    ignore_result = False
    max_retries = 0

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print 'Error: {0}, {1}, {2}, {3}, {4}'.format(
            exc, task_id, args, kwargs, einfo
        )


@app.task(base=BaseTask)
def pre_deployment_start(msg=None):
    return {
        'status': 'done',
        'message': 'Pre-deployment task start',
        'msg': msg,
    }


@app.task(base=BaseTask)
def pre_deployment_end(msg=None):
    return {
        'status': 'done',
        'message': 'Pre-deployment task end',
        'msg': msg,
        }


@app.task(base=BaseTask)
def deployment_start(msg=None):
    return {
        'status': 'done',
        'message': 'Deployment task start',
        'msg': msg,
    }


@app.task(base=BaseTask)
def deployment_end(msg=None):
    return {
        'status': 'done',
        'message': 'Deployment task end',
        'msg': msg,
    }


@app.task(base=BaseTask)
def post_deployment_start(msg=None):
    return {
        'status': 'done',
        'message': 'Post-deployment task start',
        'msg': msg,
    }


@app.task(base=BaseTask)
def post_deployment_end(msg=None):
    return {
        'status': 'done',
        'message': 'Post-deployment task end',
        'msg': msg,
        }


@app.task(base=BaseTask)
def upload_file(msg=None, filename=None):
    print 'running upload file {0}'.format(filename)

    time.sleep(1)

    return {
        'status': 'done',
        'message': 'File {0} uploaded'.format(filename),
        'msg': msg,
    }


@app.task(base=BaseTask)
def run_puppet(msg=None, puppet_module=None):
    print 'running puppet {0}'.format(puppet_module)

    time.sleep(1)

    return {
        'status': 'done',
        'message': 'Puppet module {0} executed'.format(puppet_module),
        'msg': msg,
    }


@app.task(base=BaseTask)
def error(msg=None):
    print 'Raising error'

    time.sleep(1)

    raise SyntaxError


@app.task(base=BaseTask)
def log_error(task_id):
    print 'Error encountered {0}'.format(task_id)

    result = app.AsyncResult(task_id)
    #result.get(propagate=False)

    return {
        'status': 'error',
        'message': 'Error encountered',
        'task_id': task_id,
        'traceback': result.traceback,
    }


def chain(tasks, link_error=None):
    link_error = link_error or log_error.s()

    for task in tasks:
        task.link_error(link_error)

    return celery.chain(*tasks)


def group(tasks, link_error=None):
    link_error = link_error or log_error.s()

    for task in tasks:
        task.link_error(link_error)

    return celery.group(*tasks)


def deploy():
    pre_d = group([
        upload_file.s(filename='key1'),
        upload_file.s(filename='key2'),
        chain([
            run_puppet.s(puppet_module='puppet1'),
            run_puppet.s(puppet_module='puppet2'),
        ])
    ])

    dep = chain([
        #error.s()
    ])

    post_d = group([
        upload_file.s(filename='post1'),
        run_puppet.s(puppet_module='post-module1')
    ])

    return chain([
        chain([
            pre_deployment_start.s(),
            pre_d,
            pre_deployment_end.s()
        ]),
        chain([
            deployment_start.s(),
            dep,
            deployment_end.s()
        ]),
        chain([
            post_deployment_start.s(),
            post_d,
            post_deployment_end.s()
        ])
     ])


def get_result_error(result, timeout=None):
    while result.parent:
        if result.failed():
            return result
        result = result.parent
