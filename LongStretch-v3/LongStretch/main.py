from website import create_app

# flask
# flask_login
# flask_sqlalchemy
# flask_bcrypt
# flask_wtf


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)