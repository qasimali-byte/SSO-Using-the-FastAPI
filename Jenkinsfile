pipeline {
    agent {label 'linux'}
    stages {
        stage('verify tooling') {
            steps {
                sh '''
                    docker info
                    docker version
                    docker-compose version
                    curl --version
                    '''
            }
        }
        stage('Start container'){
            steps {
                sh 'docker compose up -d --no-color --wait'
                sh 'docer compose ps'
            }
        }
        stage('Run tests') {
            steps {
                sh 'curl http://localhost:80/'
            }
        }
    }
    post {
        always {
            sh 'docker compose down'
            sh 'docker compose ps'
        }
    }
}