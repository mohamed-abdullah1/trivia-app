## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories Object, success value, and total number of categories
    
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}

```


#### GET /questions
- General:
    - Returns a list of questions Object, success value, total number of questions, and categories of these questions separated
    - - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": [
    "Sports",
    "Entertainment",
    "Geography",
    "History"
  ],
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### POST /questions/
- General:
    - Creates a new question using the question_text, its answer, difficulty score, and category id. Returns created question, message indicates the success of the operation, and total number of questions after adding the new question. 
- `curl http://127.0.0.1:5000/questions/ -X POST -H "Content-Type: application/json" -d '{"question_text":"Why...?","answer":"Because ..","difficulty":4,"category":1}'`
```
{
  "created_question": {
    "answer": "Why...?",
    "category": 1,
    "difficulty": 4,
    "id": 29,
    "question": "Because .."
  },
  "msg": "Question Has Been Created Successfully!",
  "success": true,
  "total_questions": 22
}
```
#### DELETE /questions/<question_id>
- General:
    - Delete the book of the given ID if it exists. Returns the deleted question object, total number of questions after deleting the book, and a message indicates the operation. 
- `curl -X DELETE http://127.0.0.1:5000/questions/5`
```
{
  "deleted_question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "msg": "Question Has Been Deleted Successfully!",
  "success": true,
  "total_questions": 21
}
```
#### POST /questions/search
- General:
    - Creates get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question, and total number of the returned questions. 
     
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search_text": "what"}'`
```
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "React Js ⚛",
      "category": 1,
      "difficulty": 1,
      "id": 28,
      "question": "What is the Best Front End Frame Work?"
    }
  ],
  "success": true,
  "total_fetched_questions": 9
}
```
#### GET /questions/category/<category_id>
- General:
    - get questions based on category 
    - Returns a list of questions Object of the specified question, success value, and total number of fetched questions.

- Sample: `curl http://127.0.0.1:5000/questions/category/2`

``` {
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_fetched_questions": 4
}
```


#### POST /questions/play/
- General:
    - get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions 
    - Takes the category id, and prev_question object which contains the id of the previous question. 
    - Returns the question object, and success value.
     
- `curl http://127.0.0.1:5000/questions/play/ -X POST -H "Content-Type: application/json" -d '{"category":4,"question":{"id":22}}'`
```
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}
```

## Some Handlers for error Status Code
#### `Status code 404`
- Return an object contains success value, error code, and message indicate the error.
```
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```
#### `Status code 422`
- Return an object contains success value, error code, and message indicate the error.
```
{
    "success": False,
    "error": 422,
    "message": "Make sure that the data sent in the request contains all valid fields and values beforehand."
}
```
