# Stage 1: Build the React application
FROM node:22-alpine AS frontend-builder

WORKDIR /app

# Copy package.json and package-lock.json from the frontend folder
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend application source code
COPY frontend/ ./

# Build the application
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:1.25-alpine

# Copy the Nginx configuration
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built assets from the builder stage
COPY --from=frontend-builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 