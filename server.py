from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

student_dict = {}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/index_jquery.html':
            # Otvorite i pošaljite sadržaj HTML fajla
            with open('index_jquery.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        else:
        # Parsiranje upita iz URL-a kako biste dobili vrednost indexa
            index = parse_qs(self.path[2:]).get('index', [None])[0]

            if index is None:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Bad Request: Missing index'.encode())
                return

            try:
            # Pokušaj da konvertuje index u ceo broj
                index = int(index)
            except ValueError:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Bad Request: Invalid index format'.encode())
                return

        # Pretraživanje rečnika za studenta sa datim indexom
            student = student_dict.get(index)

            if student:
            # Ako student postoji, pošaljite informacije o studentu sa statusom 200
                student_info = f'Name: {student[0]}\nLast Name: {student[1]}\nCity: {student[2]}'
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')  # Dodajte CORS zaglavlje
                self.end_headers()
                self.wfile.write(student_info.encode())
            else:
                # Ako student nije pronađen, šaljemo odgovor sa statusom 404
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')  # Dodajte CORS zaglavlje
                self.end_headers()
                self.wfile.write('Student not found'.encode())

    def do_POST(self):
        # Parsiranje tela POST zahteva kako biste dobili podatke o studentu
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        post_params = parse_qs(post_data)

        index = post_params.get('index', [None])[0]
        name = post_params.get('name', [None])[0]
        last_name = post_params.get('last_name', [None])[0]
        city = post_params.get('city', [None])[0]

        if None in [index, name, last_name, city]:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')  # Dodajte CORS zaglavlje
            self.end_headers()
            self.wfile.write('Bad Request: Missing parameters'.encode())
            return

        try:
            # Pokušaj da konvertuje index u ceo broj
            index = int(index)
        except ValueError:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')  # Dodajte CORS zaglavlje
            self.end_headers()
            self.wfile.write('Bad Request: Invalid index format'.encode())
            return

        # Dodavanje novog studenta u rečnik
        student_dict[index] = [name, last_name, city]

        # Slanje odgovora sa statusom 200 i ažuriranim rečnikom studenata
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')  # Dodajte CORS zaglavlje
        self.end_headers()
        self.wfile.write(str(student_dict).encode())

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)
    http_server = HTTPServer(server_address, RequestHandler)
    print('Server started on http://127.0.0.1:8080')
    http_server.serve_forever()
