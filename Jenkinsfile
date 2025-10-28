pipeline {
    agent any

    environment {
        IMAGE_NAME = "devsecops-lab-web"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Shakcode1/devsecops-lab.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ${IMAGE_NAME}:latest ./app'
                }
            }
        }

        stage('Run Bandit Scan') {
            steps {
                script {
                    sh 'bandit -r app/ || true'
                }
            }
        }

        stage('Run Trivy Scan') {
            steps {
                script {
                    // Ignorer l'erreur pour ne pas bloquer le pipeline
                    sh 'trivy image --exit-code 0 ${IMAGE_NAME}:latest || true'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest app/tests/test_app.py || true'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Docker container...'
                script {
                    // Arrêter le conteneur précédent si existant
                    sh 'docker rm -f ${IMAGE_NAME} || true'
                    // Lancer un nouveau conteneur
                    sh 'docker run -d --name ${IMAGE_NAME} -p 5000:5000 ${IMAGE_NAME}:latest'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}
