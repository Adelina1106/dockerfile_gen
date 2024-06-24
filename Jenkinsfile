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
                script {
            // Activate your virtual environment
            sh ". ${VIRTUAL_ENV}/bin/activate"
            
            // Pull latest changes from Git (assuming your Jenkins workspace is already set to your project directory)
            sh "git pull"
            
            // Install Python dependencies
            sh "pip install -r requirements.txt"
            
            // Run your Django server
            sh "python3 manage.py runserver"
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
