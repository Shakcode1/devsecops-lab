pipeline {
    agent {
        docker {
            image 'python:3.9-slim'   // Image contenant Python
            args '-u root:root'       // Exécuter en root (utile pour installer des paquets si besoin)
        }
    }

    environment {
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }

    stages {
        stage('Checkout') {
            steps {
                // Cloner la branche main explicitement
                git branch: 'main', url: 'https://github.com/Shakcode1/devsecops-lab.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install --upgrade pip'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '. venv/bin/activate && pytest || true'
                }
            }
        }

        stage('Static Code Analysis (Bandit)') {
            steps {
                script {
                    sh '. venv/bin/activate && bandit -r . || true'
                }
            }
        }

        stage('Container Vulnerability Scan (Trivy)') {
            steps {
                script {
                    sh 'docker-compose build'
                    sh 'trivy image ${IMAGE_NAME}:latest || true'
                }
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            steps {
                script {
                    sh '. venv/bin/activate && safety check || true'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
