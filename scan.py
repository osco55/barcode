import cv2
from pyzbar.pyzbar import decode 
import requests

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
camera = True
books=[]
last_code=0

def get_book_title(barcode):
    api_url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + barcode
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            book_title = data['items'][0]['volumeInfo']['title']
            return book_title
        else:
            return "Titre non trouvé"
    except requests.exceptions.RequestException as e:
        print("Erreur de requête :", e)
        return "Erreur de requête"
    
while camera:
    success, frame = cap.read()
    for code in decode(frame):
        code_actual = code.data.decode("utf-8")
        if code_actual !=last_code:
            books.append(get_book_title(code.data.decode("utf-8")))
        print(code.type)
        print(code.data.decode("utf-8"))
        last_code = code.data.decode("utf-8")

    cv2.imshow('test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Voici les livres que vous possédez :", books)
