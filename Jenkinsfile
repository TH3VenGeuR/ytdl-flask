pipeline {
    agent any
    environment {
                DOCKERHUB = credentials('DOCKERHUB')
    }
    stages {
        stage('Build') {
            steps {
                sh 'echo Start building'

                sh 'echo Clone repository'
                git branch: 'main', credentialsId: 'jenkins-github-key', url: 'git@github.com:disasstor/ytdl-flask.git'

                sh 'docker build -t ilyatrof/ytdl-flask:v${BUILD_NUMBER} .'

                sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'

                sh 'docker push ilyatrof/ytdl-flask:v${BUILD_NUMBER}'

                sh 'docker rmi ilyatrof/ytdl-flask:v${BUILD_NUMBER}'

                //sh 'echo configure ssh'
                //eval `ssh-agent -s`
                //sh 'ssh-add ~/.ssh/jenkins_key'
            }
        }
        stage('Deploy') {
            steps {
                script {
                    try{
                        sh 'echo Try to pulling image'
                        sh 'docker --host $DOCKER_HOST pull ilyatrof/ytdl-flask:v${BUILD_NUMBER}'

                    }catch (err) {
                        sh 'echo Pull ERROR'

                    }
                    try{
                        sh 'echo Try to kill and remove older cootainers'
                        sh 'docker --host $DOCKER_HOST kill ytdl-flask-app'
                        sh 'docker --host $DOCKER_HOST rm ytdl-flask-app'

                    }catch (err) {
                        sh 'echo Kill and remove older cootainers ERROR'

                    }
                    try{
                        sh 'echo Try to remove older image'
                        //sh 'docker --host $DOCKER_HOST rmi -f ilyatrof/ytdl-flask:v${BUILD_NUMBER-1}'

                    }catch (err) {
                        sh 'echo Remove older image ERROR'

                    }
                    try{
                        sh 'echo Try to deploy container'
                        sh 'docker --host $DOCKER_HOST run --rm --name ytdl-flask-app -d -p 5000:5000 ilyatrof/ytdl-flask:v${BUILD_NUMBER}'

                    }catch (err) {
                        sh 'echo Deploy error'

                    }
                }
            }
        }
    }
}