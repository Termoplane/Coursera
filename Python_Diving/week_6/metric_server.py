import asyncio
from itertools import groupby


metric_storage = {}

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        try:
            request_parts = data.split()
            request_name = request_parts[0]
        except IndexError:
            return 'error\nwrong command\n\n'   
        
        if request_name == 'put':
            if len(request_parts) != 4:
                return 'error\nwrong command\n\n'
            try:
                value, timestamp = float(request_parts[2]), int(request_parts[3])
            except ValueError:
                return 'error\nwrong command\n\n'
            return self._put_handler(request_parts[1], value, timestamp)

        elif request_name == 'get':
            if len(request_parts) != 2:
                return 'error\nwrong command\n\n'
            return self._get_handler(request_parts[1])

        else:
            return 'error\nwrong command\n\n'

    def _put_handler(self, metric, value, timestamp):
        if metric not in metric_storage:
            metric_storage[metric] = []
        if (value, timestamp) not in metric_storage[metric]:
            for x in range(len(metric_storage[metric])):
                if timestamp in metric_storage[metric][x]:
                    ind = x
                    metric_storage[metric][ind] = (value, timestamp)
                    
            metric_storage[metric].append((value, timestamp))

            metric_storage[metric] = [el for el, _ in groupby(metric_storage[metric])]

            metric_storage[metric].sort(key=lambda vals: vals[1])
        return 'ok\n\n'

    def _get_handler(self, metric):
        res = ''
        if metric == '*':
            for metric, values in metric_storage.items():
                for value in values:
                    res = res + metric + ' ' +str(value[0]) + ' ' + str(value[1]) + '\n'
        elif metric not in metric_storage:
            return 'ok\n\n'
        else:
            for value, timestamp in metric_storage[metric]:
                res = res + metric + ' ' + str(value) + ' ' + str(timestamp) + '\n'
        return 'ok\n' + res + '\n'

def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server()
