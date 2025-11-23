from celery import shared_task

@shared_task
def test(z,y):
    return z*y