# Use a lightweight base image
FROM golang:1.19-alpine AS builder

# Set working directory
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o wisecow

# Create final lightweight image
FROM alpine:3.17

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/wisecow .

# Expose port
EXPOSE 8080

# Run the application
CMD ["./wisecow"]