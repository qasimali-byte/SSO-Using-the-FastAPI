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
                sh 'docker-compose -f docker-compose.dev.yml up -d --build'
                sh 'docker-compose ps'
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
            sh 'docker-compose down --remove-orphans -v'
            sh 'docker-compose ps'
        }
    }
}