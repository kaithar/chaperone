import asyncio
from chaperone.cproc.subproc import SubProcess

class SimpleProcess(SubProcess):

    _fut_monitor = None

    async def process_started_co(self):
        if self._fut_monitor and not self._fut_monitor.cancelled():
            self._fut_monitor.cancel()
            self._fut_monitor = None

        # We wait a short time just to see if the process errors out immediately.  This avoids a retry loop
        # and catches any immediate failures now.

        await self.do_startup_pause()

        # If there is a pidfile, sit here and wait for a bit
        await self.wait_for_pidfile()

        # We have a successful start.  Monitor this service.

        self._fut_monitor = asyncio.ensure_future(self._monitor_service())
        self.add_pending(self._fut_monitor)

    async def _monitor_service(self):
        result = await self.wait()
        if isinstance(result, int) and result > 0:
            await self._abnormal_exit(result)
