from homework import create_app

app = create_app()

if __name__ == "__main__":
    app = create_app({'SHOWINFO': True})
    app.run(debug=True)
