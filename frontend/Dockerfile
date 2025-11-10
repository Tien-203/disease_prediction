# Frontend Dockerfile for Disease Prediction App
# Multi-stage build: Node.js for building, nginx for serving

# Stage 1: Build Angular application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json ./

# Install dependencies
# Using npm install instead of npm ci since package-lock.json may not exist
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build argument for API URL
ARG API_URL=http://backend:8000/api/v1

# Update environment file with build-time API URL
RUN printf "/*\n * Production environment configuration\n */\nexport const environment = {\n  production: true,\n  apiUrl: '%s',\n  appName: 'Disease Prediction System',\n  version: '1.0.0'\n};\n" "${API_URL}" > src/environments/environment.prod.ts

# Verify environment file was created correctly
RUN cat src/environments/environment.prod.ts

# Build Angular application
RUN npm run build -- --configuration production

# Verify build output structure
RUN echo "=== Build output structure ===" && \
    ls -la /app/dist/ && \
    echo "=== Checking for browser subdirectory ===" && \
    (ls -la /app/dist/disease-prediction-frontend/browser 2>/dev/null && echo "Browser subdirectory exists" || echo "No browser subdirectory, using direct output")

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built application from builder stage
# Check if browser subdirectory exists, otherwise use direct output
COPY --from=builder /app/dist/disease-prediction-frontend /tmp/dist-output

# Move files to nginx html directory based on actual structure
RUN if [ -d /tmp/dist-output/browser ]; then \
        cp -r /tmp/dist-output/browser/* /usr/share/nginx/html/; \
    else \
        cp -r /tmp/dist-output/* /usr/share/nginx/html/; \
    fi && \
    rm -rf /tmp/dist-output

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
