pipeline {
    agent any
    environment {
        // Set up Python and Docker
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pull the code from GitHub (branch main explicitly)
                git branch: 'main', url: 'https://github.com/Shakcode1/devsecops-lab.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Create virtual environment
                    sh 'python3 -m venv venv'
                    // Install dependencies from app/requirements.txt
                    sh 'source ./venv/bin/activate && pip install -r app/requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests with pytest on app/
                    sh 'source ./venv/bin/activate && pytest app/'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    // Run Bandit on app/
                    sh 'source ./venv/bin/activate && bandit -r app/ || true'
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker-compose build'
                    // Scan the image with Trivy
                    sh 'trivy image ${IMAGE_NAME}:latest || true'
                }
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    // Check Python dependencies for vulnerabilities
                    sh 'source ./venv/bin/activate && safety check -r app/requirements.txt || true'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Redeploy the application using Docker Compose
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            // Clean workspace after build
            cleanWs()
        }
    }
}
