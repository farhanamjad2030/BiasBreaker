# BiasBreaker

#### Video Demo: https://youtu.be/BwlPnqh9m-4

### Description
**BiasBreaker** is a decision-making web application that helps users choose between two options by implementing a weighted rating system and scores based on various criteria. The goal is to minimize emotional or biased influences during decisions. So, BiasBreaker assists you in a structured and logical way to decide between job offers, universities, or even which car to buy.

After registering and logging in, it starts with a Homepage where the user has to enter two options along with at least 1 or up to 5 criteria with associated weights. After that, the user has to rate both options against each criterion on next page. And at the end, it displays the result and suggests a choice.

> **Note:** Stylistically, the app is inspired from the `Finance` problem.


### Design choice: In-Memory storage vs. Early Database Storage
Well, at the start of the project, it was necessary to debate a key architectural decision: whether to store user input immediately/directly into the database or to temporarily hold the information in memory and store it only at the end of the comparison process. I opted for the latter i.e., storing data in memory (via POST requests and template rendering) until the final decision is made.

#### Design 1: Store immediately in the Database
- #### Strengths
    - This design ensures that every step of user's input is constantly recorded.
    - It helps to track partial user-progress and to recover from unexpected exits.
- #### Weaknesses
    - As a consequence, the process results in frequent and redundant writes to the database.
    - It adds complexity to handle incomplete decision processes.
    - It requires some cleanup mechanism for temporary or partial data.

#### Design 2: Store in Memory First (Chosen Approach)
- #### Strengths
    - This design keeps the database clean by storing only finalized and meaningful data.
    - It Simplifies logic and schema, as only complete decisions are recorded.
    - It reduces unnecessary database I/O operations, improving performance.
- #### Weaknesses:
    - Temporary data is lost if the session expires or the user (accidentally) closes the tab.
    - If I want to grow the app in future (e.g., multiple comparison rounds), memory-only storage may become a bad design solution.

#### Why I chose this Design
As BiasBreaker is a structured, user-driven web application, so the final results over partial inputs are prioritized. Also, users are only expected to store a decision once they've rated all criteria and are ready to view the result. This makes the memory-first approach ideal: it's lightweight, user-centric, and reduces database clutter.


### Features
- **User Authentication:** Lets users to register and log in to access the app and history individually.
- **Criteria Based:** Lets the user input two options to compare and specify up to five decision criteria with associated weights.
- **Weighted Rating:** Lets the user rate both options against each criterion. The app computes a weighted score for each and declares a "winner".
- **History Tracking:** Stores all past decisions that are viewable via a dedicated history page.


### File Overview

#### `app.py`
This is the backend of the application. It is written in Python and it uses the Flask framework. Also it defines all the routes and logic, including:

- `/` – Home page, only accessible when logged in.
- `/login` – Allows users to log into their accounts.
- `/logout` – Logs the user out by clearing the session.
- `/register` – Handles new user registration.
- `/compare` – Takes two user-defined options and up to five criteria with weights, then passes this to the next step.
- `/result` – Collects ratings for each option against the defined criteria, computes total weighted scores, determines the winner, stores the result in the database, and displays the outcome.
- `/history` – Displays a user's past decision comparisons.

#### Templates
- `apology.html` – Handles/Renders error messages.
- `layout.html` – Main layout of the whole web application.
- `index.html` – The Homepage or landing page after login.
- `login.html` and `register.html` – For user authentication.
- `ratings.html` – To gather ratings from the user for each option.
- `result.html` – Displays comparison results and the Winner.
- `history.html` – Shows stored decisions for the logged-in user.

#### Static
- `ChatGPT_Image_Jun_20__2025__01_14_06_AM.png` – An image to use as `favicon`.

- `styles.css` – A stylesheet to apply CSS to certain elements besides `Bootstrap`.

#### `helpers.py`
This file is used to define utility/helper functions:
- `apology(message)` – Returns an error page with the given message.
- `login_required` – A decorator to restrict certain routes to authenticated users only.

#### `biasbreaker.db`
This is the SQLite database to store information. It includes:
- A `users` table with user credentials.
- A `decisions` table that records the user ID, both options, the winning choice, and a timestamp.
