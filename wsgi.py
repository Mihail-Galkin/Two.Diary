from dotenv import load_dotenv

from app import create_app

app = create_app()
load_dotenv('.env')

if __name__ == "__main__":
    app.run()
