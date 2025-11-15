import socket
import mimetypes
import pathlib
import urllib.parse
import json
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server parameters
HTTP_PORT = 3000
SOCKET_HOST = '0.0.0.0'
SOCKET_PORT = 5000
BUFFER_SIZE = 1024

# Path to static files
BASE_DIR = pathlib.Path(__file__).parent
FRONT_DIR = BASE_DIR / 'front'


class HttpHandler(BaseHTTPRequestHandler):
    """HTTP request handler"""

    def do_GET(self):
        """Handle GET requests"""
        pr_url = urllib.parse.urlparse(self.path)
        
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        elif pr_url.path == '/style.css':
            self.send_static('style.css')
        elif pr_url.path == '/logo.png':
            self.send_static('logo.png')
        else:
            self.send_html_file('error.html', 404)

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/message':
            data = self.rfile.read(int(self.headers['Content-Length']))
            self.send_data_to_socket(data)
            
            # Redirect to home page after sending
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        """Send HTML file"""
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        file_path = FRONT_DIR / filename
        try:
            with open(file_path, 'rb') as fd:
                self.wfile.write(fd.read())
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            self.wfile.write(b'404 Not Found')

    def send_static(self, filename):
        """Send static files"""
        file_path = FRONT_DIR / filename
        
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            logging.error(f"Static file not found: {file_path}")
            self.send_html_file('error.html', 404)

    def send_data_to_socket(self, data):
        """Send data to Socket server"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
            client_socket.close()
            logging.info(f"Data sent to socket server: {data}")
        except Exception as e:
            logging.error(f"Error sending data to socket server: {e}")


def run_http_server():
    """Start HTTP server"""
    server_address = ('0.0.0.0', HTTP_PORT)
    http = HTTPServer(server_address, HttpHandler)
    logging.info(f"Starting HTTP server on port {HTTP_PORT}")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        logging.info("HTTP server stopped")
    finally:
        http.server_close()


def save_to_mongodb(data):
    """Save data to MongoDB"""
    try:
        # Connect to MongoDB
        mongo_uri = "mongodb://mongodb:27017/"
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        
        db = client.messages_db
        collection = db.messages
        
        # Insert document
        collection.insert_one(data)
        logging.info(f"Message saved to MongoDB: {data}")
        
        client.close()
    except Exception as e:
        logging.error(f"Error saving to MongoDB: {e}")


def run_socket_server():
    """Start Socket server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SOCKET_HOST, SOCKET_PORT))
    logging.info(f"Starting Socket server on port {SOCKET_PORT}")
    
    try:
        while True:
            data, address = server_socket.recvfrom(BUFFER_SIZE)
            logging.info(f"Received data from {address}: {data}")
            
            try:
                # Parse form data
                data_parse = urllib.parse.unquote_plus(data.decode())
                data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
                
                # Add timestamp
                data_dict['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                
                logging.info(f"Parsed data: {data_dict}")
                
                # Save to MongoDB
                save_to_mongodb(data_dict)
                
            except Exception as e:
                logging.error(f"Error processing data: {e}")
                
    except KeyboardInterrupt:
        logging.info("Socket server stopped")
    finally:
        server_socket.close()


if __name__ == '__main__':
    # Start HTTP and Socket servers in different threads
    http_thread = Thread(target=run_http_server, name='HTTP-Server', daemon=True)
    socket_thread = Thread(target=run_socket_server, name='Socket-Server', daemon=True)
    
    http_thread.start()
    socket_thread.start()
    
    try:
        http_thread.join()
        socket_thread.join()
    except KeyboardInterrupt:
        logging.info("Shutting down servers...")
