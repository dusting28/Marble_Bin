from website import create_app

app = create_app()

if __name__ == '__main__':
    # Set Debug to False when deploying (keep at True) during development
    app.run(debug=True)
