import webhook, webserver
import threading, sys

thread_webhook = threading.Thread(target=webhook.run)
thread_webserver = threading.Thread(target=webserver.run)

if __name__ == '__main__':
    try:
        thread_webhook.start()
        thread_webserver.start()        
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
