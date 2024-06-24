pipeline {
    agent any
    environment {
        VIRTUAL_ENV = "${WORKSPACE}/env"
    }
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main',  // Specify the branch 'main' here
                    credentialsId: 'docker',
                    url: 'git@github.com:Adelina1106/dockerfile_gen.git'
            }
        }
        stage('Setup Environment') {
            steps {
                script {
                    if (!fileExists("${VIRTUAL_ENV}")) {
                        sh 'python3 -m venv env'
                    }
                }
                sh """
                . env/bin/activate
                echo 'student' | sudo -S apt-get update
                echo 'student' | sudo -S apt-get install -y libmysqlclient-dev
                # Replace <your_sudo_password> with the actual password (not recommended for production use)
                
                pip install --upgrade pip
                pip install -r requirements.txt
                """
                    }
        }
        stage('Run Tests') {
            steps {
                sh """
                . ${VIRTUAL_ENV}/bin/activate
                python manage.py test
                """
            }
        }
        stage('Deploy') {
            steps {
                sshagent(['docker']) {
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
