# Library Management System

## Description
The Library Management System is a web application that allows users to manage books and borrowers in a library. It provides functionalities such as adding, updating, and deleting books, as well as borrowing books.

## Installation
1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `python setup.py`

## Usage
1. Start the FastAPI server: `uvicorn main:app --reload`
2. Open your web browser and go to `http://localhost:8000` to access the API documentation.

## API Endpoints
- `GET /api/books`: Get all books
- `GET /api/books/{id}`: Get a book by ID
- `POST /api/books`: Add a new book
- `PUT /api/books/{id}`: Update a book
- `DELETE /api/books/{id}`: Delete a book
- `POST /api/books/{id}/{borrower_id}`: Borrow a book

## Configuration
- Database URL: Set the database URL in the `.env` file
- FastAPI configuration: Modify the `main.py` file to change the FastAPI settings

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature`)
6. Create a new Pull Request



## Credits
- [@BrightTonny](https://github.com/BrightTonny)
- [@kweku_tb](https://github.com/kweku_tb)
