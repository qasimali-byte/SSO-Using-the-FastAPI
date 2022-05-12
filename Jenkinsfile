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
                sh 'docker-compose -f docker-compose.dev.yml down'
                sh 'docker-compose -f docker-compose.dev.yml up -d --build'
                sh 'docker ps'
            }
        }
        stage('Run tests') {
            steps {
                sh 'curl http://localhost:80/'
            }
        }
    }
    // post {
    //     always {
    //         sh 'docker ps -a -q |sudo  xargs docker stop' 
    //         sh 'docker-compose ps'
    //     }
    // }
}