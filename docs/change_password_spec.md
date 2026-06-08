# Feature Specification: Change Password

## 1. User Stories
- As a user, I want to be able to change my own password to maintain account security.
- As an administrator, I want to be able to change my own password and the passwords of other users for administrative purposes.

## 2. Technical Specification

### 2.1 API Endpoints

#### `PATCH /users/me/password`
- **Description**: Updates the password of the currently authenticated user.
- **Authentication**: Required (JWT).
- **Request Body**:
  ```json
  {
    "current_password": "string",
    "new_password": "string"
  }
  ```
- **Validation**:
    - `current_password` must be provided and match the stored hashed password.
    - `new_password` must be at least 8 characters long.
- **Responses**:
    - `200 OK`: Password successfully updated.
    - `400 Bad Request`: Validation error (e.g., password too short).
    - `401 Unauthorized`: Current password does not match.

#### `PATCH /users/{user_id}/password`
- **Description**: Updates the password of a specific user.
- **Authentication**: Required (JWT).
- **Authorization**: Requires `admin` role.
- **Request Body**:
  ```json
  {
    "new_password": "string"
  }
  ```
- **Validation**:
    - `new_password` must be at least 8 characters long.
- **Responses**:
    - `200 OK`: Password successfully updated.
    - `400 Bad Request`: Validation error.
    - `403 Forbidden`: Insufficient permissions (non-admin).
    - `404 Not Found`: User with given `user_id` not found.

### 2.2 Backend Logic
- **Hashing**: New passwords must be hashed using the project's existing hashing utility before storage.
- **Security**: 
    - Passwords must never be logged or returned in API responses.
    - The `current_password` check for self-service changes must be performed using a secure constant-time comparison.
- **Session Invalidation**: Changing a password must invalidate all existing JWTs for that user. This should be implemented by updating a `token_version` or `password_changed_at` field in the `users` table and verifying it against the token's issuance date.

### 2.3 Frontend Requirements
- **User Interface**:
    - A "Change Password" form in the user settings/profile area.
    - A "Change Password" button/modal in the Admin User Management view (`frontend/src/views/admin/UsersView.vue`).
- **Client-side Validation**:
    - Ensure the `new_password` field has a minimum length of 8 characters before submitting the request.
- **User Experience**:
    - On successful password change, the user should be notified and redirected to the login page (since the current token is invalidated).

## 3. Assumptions
1. The user must provide their current password to change their own password.
2. The administrator can change the password of other users without knowing their current password.
3. The minimum password length is 8 characters.
4. No email notifications are sent after a password change.
5. A password change forces a logout by invalidating the current JWT.
