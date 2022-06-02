import json
import logging
import coloredlogs
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory


logger = logging.getLogger("notifications")
coloredlogs.install(level='DEBUG', logger=logger)


class TestServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        logger.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logger.info("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            result = self.onMessageBinary(payload)
        else:
            payload = payload.decode("utf-8")
            try:
                payload = json.loads(payload)
            except:
                result = self.onMessageText(payload)
            else:
                result = json.dumps(self.onMessageJson(payload))
            result = result.encode("utf-8")
        self.sendMessage(result, isBinary)

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
        logger.info("client exiting, {0}".format(self.peer))
        logger.info("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':
    import asyncio

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = TestServerProtocol

    event_loop = asyncio.get_event_loop()
    coroutine = event_loop.create_server(factory, '0.0.0.0', 9000)
    server = event_loop.run_until_complete(coroutine)

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        event_loop.close()

