License Plate Recognition

1. Install Django, Python and Docker in your local machine.
2. In your project root directory run pip install -r requirements.txt
3. Create your own .env file at the root directory of the project and paste the contents of .env.template in it.
4. Fetch ANPR_ENDPOINT, ANPR_API_USER and ANPR_API_PASSWORD from the admin, in this case ME.
5. To run the project locally execute: uvicorn main:app --reload
6. To run the project locally on a Docker container, run docker-compose build --no-cache then docker-compose up
