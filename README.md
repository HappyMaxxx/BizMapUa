# BizMapUa

BizMapUa is a web application developed for the **ITREVOLUTION'25 Hackathon**. It provides a platform for users to discover, create, and rate businesses across various regions of Ukraine. The application allows users to register, log in, add businesses with photos, and filter businesses by categories, cities, and tags. It also includes an admin panel for managing pending businesses and a rating system for user feedback.

## Features
- **User Authentication**: Register and log in to access personalized features.
- **Business Creation**: Authenticated users can create businesses with details and photos.
- **Business Filtering**: Filter businesses by region, category, city, or tags with sorting options (e.g., popularity).
- **Rating System**: Users can rate businesses, and the average rating is updated dynamically.
- **Admin Panel**: Staff users can approve or decline pending businesses.
- **Responsive Design**: The application is designed to work seamlessly across devices.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Django ORM with PostgreSQL
- **Authentication**: Django's built-in authentication system
- **Containerization**: Docker and Docker Compose
- **Deployment**: Configurable for platforms like Heroku, AWS, or local servers via Docker

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## Installation

### Using Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/HappyMaxxx/BizMapUa.git
   ```
2. Navigate to the project directory:
   ```bash
   cd BizMapUa
   ```
3. Create a `.env` file in the project root with the following (adjust as needed):
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1,your-allowed-hosts

   POSTGRES_DB=app_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   ```
4. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
5. Apply database migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
6. Access the application at `http://127.0.0.1:8000`.

## Example Docker Compose File
Create a `docker-compose.yml` file in the project root if it doesn't exist:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_db
      
    command: ["./wait-for-it.sh", "db:5432", "--", "python3", "manage.py", "runserver", "0.0.0.0:8000"]

  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

> **Note**: The [`wait-for-it.sh`](https://github.com/vishnubob/wait-for-it) script ensures the web service waits for the PostgreSQL database to be ready. It is included in the repository.

## Example Dockerfile
The `Dockerfile` in the project root:

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Project Structure
- `hackaton/`: Django project root with settings, URLs, and WSGI/ASGI configurations.
- `mainapp/`: Main application with models, views, forms, and templates.
  - `models.py`: Defines models like `Region`, `Businesse`, `BuisnessePhoto`, and `Evaluation`.
  - `views.py`: Handles authentication, business creation, filtering, and rating logic.
  - `forms.py`: Includes forms for user registration, login, and business creation.
  - `templates/mainapp/`: HTML templates for pages like homepage, profile, and business views.
  - `static/mainapp/`: CSS, JavaScript, and images for frontend styling and functionality.
- `media/`: Stores uploaded files (e.g., business photos, region images).
- `w_supporting/`: Contains scripts (`oblast_pars.py`) and GeoJSON data (`parsed_ukraine_geojson.json`) for map features.
- `requirements.txt`: Lists Python dependencies.
- `wait-for-it.sh`: Utility script to ensure database availability.

## Usage
- **Register/Login**: Create an account or log in to access features like business creation and rating.
- **Create a Business**: Navigate to the "Create Business" page, fill in details, and upload photos.
- **Browse Businesses**: Use the map or region view to filter and sort businesses.
- **Admin Panel**: Staff users can access `/adminpanel` to manage pending businesses.
- **Rate Businesses**: Authenticated users can rate businesses, which updates the average rating.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License.

## Developers
This project was built by a dedicated team for the ITREVOLUTION'25 Hackathon:
- **Designer**: insta: @annimilet - Responsible for the UI/UX design and visual aesthetics.
- **Frontend Developer**: insta: @twinkell0 - Implemented the frontend templates and client-side interactivity.
- **Backend Developer**: insta: @vmzxgh - Developed the backend logic, database models, and API endpoints.