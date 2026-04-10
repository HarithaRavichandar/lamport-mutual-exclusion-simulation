from lamport_clock import LamportClock

class Process:
    def __init__(self, env, pid, processes, log):
        self.env = env
        self.pid = pid
        self.clock = LamportClock()
        self.processes = processes
        self.request_queue = []
        self.replies_received = set()
        self.log = log
        self.requesting = False
        self.my_request = None  # store own request

    def send_request(self):
        self.clock.tick()
        timestamp = self.clock.time

        self.my_request = (timestamp, self.pid)
        self.request_queue.append(self.my_request)

        # Sort queue (Lamport ordering: timestamp, then PID)
        self.request_queue.sort()

        self.requesting = True
        self.replies_received = set()

        self.log.append(f"Time {self.env.now}: P{self.pid} REQUEST at t={timestamp}")

        for p in self.processes:
            if p.pid != self.pid:
                p.receive_request(timestamp, self.pid)

    def receive_request(self, timestamp, sender_pid):
        self.clock.update(timestamp)

        self.request_queue.append((timestamp, sender_pid))
        self.request_queue.sort()

        self.log.append(f"Time {self.env.now}: P{self.pid} received REQUEST from P{sender_pid}")

        # Send reply immediately
        for p in self.processes:
            if p.pid == sender_pid:
                p.receive_reply(self.pid)

    def receive_reply(self, sender_pid):
        self.replies_received.add(sender_pid)
        self.log.append(f"Time {self.env.now}: P{self.pid} received REPLY from P{sender_pid}")

    def send_release(self):
        self.clock.tick()
        self.requesting = False

        self.log.append(f"Time {self.env.now}: P{self.pid} RELEASE")

        # Remove own request
        self.request_queue = [req for req in self.request_queue if req != self.my_request]

        for p in self.processes:
            if p.pid != self.pid:
                p.receive_release(self.pid)

    def receive_release(self, sender_pid):
        self.request_queue = [req for req in self.request_queue if req[1] != sender_pid]
        self.log.append(f"Time {self.env.now}: P{self.pid} received RELEASE from P{sender_pid}")

    def can_enter_cs(self):
        if not self.requesting:
            return False

        # Must receive replies from all
        if len(self.replies_received) != len(self.processes) - 1:
            return False

        # Must be first in sorted queue
        return self.request_queue[0] == self.my_request

    def run(self):
        while True:
            # Stagger process start (IMPORTANT)
            yield self.env.timeout(self.pid)

            self.send_request()

            # WAIT phase
            while not self.can_enter_cs():
                yield self.env.timeout(0.5)

            # ENTER CS
            self.log.append(f"Time {self.env.now}: P{self.pid} ENTER CS")
            yield self.env.timeout(3)

            # EXIT CS
            self.log.append(f"Time {self.env.now}: P{self.pid} EXIT CS")
            self.send_release()

            yield self.env.timeout(5)