pipeline {
    agent any
    environment {
        VIRTUAL_ENV = "${WORKSPACE}/env"
    }
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main',
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
                
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install gunicorn
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
                    // Pull latest changes from Git
                    checkout([$class: 'GitSCM',
                              branches: [[name: 'main']],
                              doGenerateSubmoduleConfigurations: false,
                              extensions: [],
                              userRemoteConfigs: [[credentialsId: 'docker',
                                                  url: 'git@github.com:Adelina1106/dockerfile_gen.git']]])

                    // Install Python dependencies
                    sh """
                    . ${VIRTUAL_ENV}/bin/activate
                    pip install -r requirements.txt
                    """
                    
                    // Run Django application with Gunicorn in the background
                    sh """
                    . ${VIRTUAL_ENV}/bin/activate
                    gunicorn --workers 3 --bind 0.0.0.0:8000 core.wsgi:application &
                    """
                }
                
                // Optional: Wait for a specific amount of time (e.g., 5 minutes) to simulate user activity
                script {
                    sleep(time: 10, unit: 'MINUTES')
                }

                // Stop the Gunicorn process after the timeout
                script {
                    def gunicorn_pid = sh(script: "pgrep -f 'gunicorn'", returnStdout: true).trim()
                    if (gunicorn_pid) {
                        sh "kill -9 ${gunicorn_pid}"
                    }
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
