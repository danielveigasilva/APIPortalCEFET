from apicefet import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)  # para prod, ative aqui!
    # app.run(debug=True, host='127.0.0.1', port=port)  # para dev, ative aqui!
