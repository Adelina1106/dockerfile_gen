pipeline {
    agent any
    environment {
        VIRTUAL_ENV = "${WORKSPACE}/env"
    }
    stages {
        stage('Clone repository') {
            steps {
                git 'git@github.com:Adelina1106/dockerfile_gen.git'
            }
        }
        stage('Setup Environment') {
            steps {
                script {
                    if (!fileExists("${VIRTUAL_ENV}")) {
                        sh 'python3 -m venv venv'
                    }
                }
                sh """
                source ${VIRTUAL_ENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }
        stage('Run Tests') {
            steps {
                sh """
                source ${VIRTUAL_ENV}/bin/activate
                python manage.py test
                """
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['your-ssh-credentials-id']) {
                    sh """
                    source ${VIRTUAL_ENV}/bin/activate
                    # Add commands to deploy your application here
                    # Example:
                    ssh Adelina1106@loocalhost:8080 'cd / && git pull && source env/bin/activate && pip install -r requirements.txt && python3 manage.py runserver'
                    """
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
