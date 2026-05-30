# Stage 1: Explicitly build and compile inside Maven
FROM maven:3.8.8-eclipse-temurin-17 AS build
WORKDIR /app

# 1. Copy the POM file
COPY pom.xml .

# 2. Copy the entire src tree preserving the subdirectory matrix explicitly
COPY src ./src

# 3. Clean and package the application
RUN mvn clean package -DskipTests

# Stage 2: Clean JRE Execution Layer
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8001
ENTRYPOINT ["java", "-jar", "app.jar"]