import asyncio
import contextlib
import uuid


class Jobs:
    def __init__(self, store):
        self.store = store
        self.tasks = {}

    def start(self, operation, work, inputs=None):
        job_id = uuid.uuid4().hex
        self.store.save_job(job_id, operation, inputs)

        def check():
            if self.store.job(job_id)['cancel']:
                raise asyncio.CancelledError()

        def progress(value):
            check()
            self.store.update_job(job_id, 'running', progress=value)

        async def run():
            try:
                check()
                self.store.update_job(job_id, 'running')
                result = await work(check, progress)
                check()
                self.store.update_job(job_id, 'succeeded', result=result, progress=1)
            except asyncio.CancelledError:
                self.store.update_job(job_id, 'cancelled', error='Cancelled; inspect any committed partial changes')
            except Exception as exc:
                # Third-party errors can contain request bodies or credentials.
                message = str(exc) if type(exc) is ValueError else f'{type(exc).__name__}: dependency/provider failure; run health and check configuration'
                self.store.update_job(job_id, 'failed', error=message)
            finally:
                self.tasks.pop(job_id, None)

        self.tasks[job_id] = asyncio.create_task(run())
        return {'job_id': job_id, 'status': 'queued'}

    def cancel(self, job_id):
        job = self.store.job(job_id)
        if job['status'] in {'queued', 'running'}:
            with self.store.connection() as db:
                db.execute('UPDATE jobs SET cancel=1 WHERE id=?', (job_id,))
        return self.store.job(job_id)

    async def close(self):
        for task in list(self.tasks.values()):
            task.cancel()
        for task in list(self.tasks.values()):
            with contextlib.suppress(asyncio.CancelledError):
                await task
