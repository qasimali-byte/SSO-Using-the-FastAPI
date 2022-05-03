stage ('Deploy') {
    steps{
        sshagent(credentials : ['faisal']) {
            sh 'ssh -o StrictHostKeyChecking=no faisal@18.134.217.103 uptime'
            sh 'ssh -v faisal@18.134.217.103'
            sh 'scp ./source/filename faisal@18.134.217.103:/remotehost/target'
        }
    }
}