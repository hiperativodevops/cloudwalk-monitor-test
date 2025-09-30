from flask import Flask

app = Flask(__name__)

@app.route('/')
def status_check():
	return 'O servidor Flask para o sistema de monitoramento está OK!'

if __name__ == '__main__':
	#Rodar o servidor. O debug=True permite que ele recarregue automaticamente.
	app.run(debug=True)