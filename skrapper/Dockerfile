# Use a base image with Java and Maven pre-installed
FROM maven:3.6.3-jdk-8 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the POM file and download the dependencies
COPY pom.xml .


# Copy the source code to the container
COPY . .

# Build the application
RUN mvn package

# Create a smaller image for the final application
FROM openjdk:8-jre-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the JAR file from the previous build stage
COPY --from=build /app/target/your-artifact-id-*.jar app.jar

# Start the application when the container runs
CMD ["java", "-jar", "app.jar"]