from homework import create_app

app = create_app({'SHOWINFO': True})

if __name__ == "__main__":
    app.run(debug=True)
