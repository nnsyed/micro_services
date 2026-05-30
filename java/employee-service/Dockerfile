# Stage 1: Build with Maven
FROM maven:3.8.8-eclipse-temurin-17 AS build
WORKDIR /app

# Copy pom.xml
COPY pom.xml .

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Stage 2: Runtime with JRE
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Copy the built JAR from build stage
COPY --from=build /app/target/employee-service-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8001
ENTRYPOINT ["java", "-jar", "app.jar"]
