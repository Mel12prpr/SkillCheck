# QuizApp

QuizApp is a web application that allows users to create, take, and manage quizzes. The application uses OpenAI's GPT-4o-mini model to generate and evaluate quiz questions and answers.

## Features

- **Create Quizzes**: Users can create quizzes by specifying the number of questions, difficulty level, and focus area.
- **Take Quizzes**: Users can take quizzes and submit their answers.
- **Automatic Grading**: The application uses OpenAI's GPT-4o-mini model to evaluate the correctness of the answers.
- **View Results**: Users can view their quiz attempts and scores.
- **Manage Quizzes**: Users can view and manage the quizzes they have created.

## Technologies Used

- **Python**: The main programming language used for the backend.
- **Django**: The web framework used to build the application.
- **OpenAI GPT-4o**: The AI model used for generating and evaluating quiz questions and answers.
- **HTML/CSS/Javascript**: For the frontend templates and styling.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mamula2023/SkillCheck.git
    cd SkillCheck 
    ```

2. Create a virtual environment and activate it:
   ```sh
    python3 -m venv venv
    source venv/bin/activate
   ``` 
   
   * Alternatively, Create and activate a virtual environment using Conda:

       ```sh
       conda create --name quizapp_env python=3.9
       conda activate quizapp_env
       ```
  
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

- **Creating a Quiz**: Navigate to the quiz creation page, fill out the form, and submit to generate quiz questions.
- **Taking a Quiz**: Select a quiz from the list of available quizzes, answer the questions, and submit.
- **Viewing Results**: After submitting a quiz, view your score and the correct answers.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.