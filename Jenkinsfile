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
        // stage ('testing') {
        //   steps {
        //     sh 'ls'
        //     sh 'echo Attech@789 | sudo -S -k virtualenv env'
        //     sh 'source ./env/bin/activate'
        //     sh 'pip3 install -r requirements.txt'
        //     sh 'python3 tests_development.py' 
        //   }
        // }
        // Edited 24-01-2023
        // stage('Start container'){
        //     steps {
        //         sh 'docker-compose down'
        //         sh 'docker-compose up -d --build'
        //         sh 'docker ps'
        //     }
        // }
        stage('Start container'){
    steps {
        sh 'docker-compose stop app'
        sh 'docker-compose up -d --build app'
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