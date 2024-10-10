# Cave Game Guide - Website

**Cave Game Guide** is a Flask-based web application for users to register, log in, and access Minecraft-related tutorials, courses, and content. The application handles user authentication, course management, and email verification for new accounts.

## Features

- **User Authentication**: Allows users to register and log in with secure hashed passwords.
- **Email Verification**: Users must verify their email addresses before activating their accounts.
- **Session Management**: Sessions are maintained using Flask's session management and expire after 30 minutes of inactivity.
- **Course Management**: Displays available courses related to Minecraft automation and building techniques.
- **Secure Password Handling**: Passwords are hashed using SHA-256 before being stored in the database.
- **SQLite Database**: Stores user information in a lightweight SQLite database.
- **Email Integration**: Sends email verifications using a custom email-sending module (`emailpy`) with a configurable email password.

## Project Structure

- **Flask Application**: The main application logic is handled by Flask.
- **SQLite Database**: User data, including usernames and hashed passwords, is stored in an SQLite database (`Database.db`).
- **JSON Configurations**: Course information is loaded from JSON files (`course_info.json`).
- **Email System**: Verification emails are sent using the `emailpy` module.

## Requirements

- **Python 3.x**
- **Flask**: The web framework for handling routes, sessions, and rendering templates.
- **SQLite3**: For storing user account data.
- **Hashlib**: Used to securely hash user passwords.
- **Random**: Generates random strings for email verification.
- **Emailpy**: Custom email-sending module for email verification.
- **HTML Templates**: Flask renders different HTML templates for the homepage, login, register, and course views.

## How It Works

1. **User Registration**:
   - The user fills out the registration form, providing a username, email, and password.
   - A verification email with a unique code is sent to the provided email address.
   - Once the user clicks the verification link, the account is activated.

2. **User Login**:
   - Users log in with their username and password.
   - Passwords are securely hashed before being compared with the stored hash in the database.

3. **Dashboard**:
   - Once logged in, users can access the dashboard, which shows the courses they are enrolled in.
   - The dashboard dynamically loads course information based on the user’s progress and stored course data.

4. **Session Management**:
   - Sessions are stored and maintained using Flask's session management.
   - The session timeout is set to 30 minutes of inactivity.

5. **Email Verification**:
   - An email containing a verification link is sent to the user during registration.
   - The link includes a unique code that validates the user's account.

6. **Course Display**:
   - Available courses are displayed on the dashboard once the user logs in.
   - Course content is stored in JSON files and displayed based on the user's progress.


## Credits
  - Backend - OCSYT
  - Frontend - MOS6502DIP
  - Database -  MITSIDOG
