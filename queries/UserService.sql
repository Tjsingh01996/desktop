-- name: GetUser :one
SELECT * FROM User
WHERE id = ? LIMIT 1;

-- name: GetUserByEmail :one
SELECT * FROM User
WHERE email = ? LIMIT 1;

-- name: VerifyUser :one
SELECT * FROM User
WHERE email = ? and name = ? LIMIT 1;

-- name: FindAll :many
SELECT * FROM User
ORDER BY name;

-- name: CreateUser :execresult
INSERT INTO User (name, email)
VALUES (?, ?);