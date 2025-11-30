# Frontend Dockerfile for Disease Prediction App
# Development server using ng serve

FROM node:18-alpine

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
RUN printf "/*\n * Development environment configuration\n */\nexport const environment = {\n  production: false,\n  apiUrl: '%s',\n  appName: 'Disease Prediction System',\n  version: '1.0.0'\n};\n" "${API_URL}" > src/environments/environment.ts

# Verify environment file was created correctly
RUN cat src/environments/environment.ts

# Expose Angular dev server port
EXPOSE 4200

# Start Angular development server
# --host 0.0.0.0 makes it accessible from outside the container
# --disable-host-check allows connections from any host
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--disable-host-check"]
