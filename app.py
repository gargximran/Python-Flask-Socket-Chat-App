from Application import create_app, socket

app = create_app(debug=True)

if __name__ == '__main__':
    socket.run(app)
