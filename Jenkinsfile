pipeline {
    agent any
    environment {
        // Set up Python and Docker
        PYTHON_IMAGE = 'python:3.9-slim'
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }
    stage('Checkout') {
    steps {
        // Pull the code from GitHub (branch main explicitly)
        git branch: 'main', url: 'https://github.com/Shakcode1/devsecops-lab.git'
    }
}

        stage('Install Dependencies') {
            steps {
                script {
                    // Install Python dependencies
                    sh 'python3 -m venv venv'
                    sh 'source ./venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run the tests with pytest
                    sh 'source ./venv/bin/activate && pytest'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    // Run Bandit for static code analysis
                    sh 'source ./venv/bin/activate && bandit -r . || true'
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
                    // Run Safety to check dependencies
                    sh 'source ./venv/bin/activate && safety check || true'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image (already done for Trivy, but we keep cette étape)
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Deploy the application using Docker Compose
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                }
            }
        }
    }
    post {
        always {
            // Clean up after build
            cleanWs()
        }
    }
}
