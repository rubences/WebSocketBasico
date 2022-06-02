import asyncio
import json
import logging
import coloredlogs
from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory


logger = logging.getLogger("notifications")
coloredlogs.install(level='DEBUG', logger=logger)


class TestClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        logger.info("Server connected: {0}".format(response.peer))

    async def onOpen(self):
        logger.info("WebSocket connection open.")

        while True:
            self.sendMessage(json.dumps({"k": "v"}).encode('utf8'))
            self.sendMessage("Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            await asyncio.sleep(5)

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.onMessageBinary(payload)
        else:
            payload = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
            except:
                self.onMessageText(payload)
            else:
                self.onMessageJson(payload)

    def onMessageBinary(self, payload):
        logger.debug("Binary message received: {0} bytes".format(len(payload)))
        return payload

    def onMessageText(self, payload):
        logger.debug("Text message received: {0}".format(payload))
        return payload

    def onMessageJson(self, payload):
        logger.debug("JSON message received: {0}".format(payload))
        return payload

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = TestClientProtocol

    event_loop = asyncio.get_event_loop()
    coroutine = event_loop.create_connection(factory, '127.0.0.1', 9000)
    event_loop.run_until_complete(coroutine)
    event_loop.run_forever()
    event_loop.close()

