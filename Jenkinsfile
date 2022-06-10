pipeline {
    agent any
    environment {
                DOCKERHUB = credentials('DOCKERHUB')
    }
    stages {
		stage('PreBuild') {
            steps {
				sh 'echo Clone repository'
                git branch: 'main', credentialsId: 'jenkins-github-key', url: 'git@github.com:disasstor/ytdl-flask.git'
			}
		}
        stage('Build') {
            steps {
                sh """
				echo Start building image
				docker build -t ilyatrof/ytdl-flask:v${BUILD_NUMBER} .
				echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin
				docker push ilyatrof/ytdl-flask:v${BUILD_NUMBER}
				"""
            }
        }
        stage('PreDeploy') {
            steps {
				script {
					def old_container_id_list = (sh(returnStdout: true, script: "docker --host $DOCKER_HOST ps -a | grep ilyatrof/ytdl-flask | awk '{ print \$1 }'")).replace("\n", " ")
					if (old_container_id_list) {	
						sh """
						echo Try to kill cootainers
						docker --host $DOCKER_HOST kill $old_container_id_list
						"""
                    }
					def old_images_id_list = (sh(returnStdout: true, script: "docker --host $DOCKER_HOST images | grep ilyatrof/ytdl-flask | awk '{ print \$3 }'")).replace("\n", " ")
					if (old_images_id_list) {	
						sh """
						echo Try to remove image
						docker --host $DOCKER_HOST rmi -f $old_images_id_list
						"""
					}
                }
            }
        }
		stage('Deploy') {
			steps {
				sh """
				echo Deploy new container
                docker --host $DOCKER_HOST run --rm --name ytdl-flask-app -d -p 5000:5000 ilyatrof/ytdl-flask:v${BUILD_NUMBER}
				"""
			}
		}
	}
}