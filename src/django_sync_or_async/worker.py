from gunicorn.workers import ggevent


class GeventWorker(ggevent.GeventWorker):
    pass
    # def patch(self):
    #     # Do not patch anything
    #     pass
