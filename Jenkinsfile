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
                sh '''
				echo Start building image
				docker build -t ilyatrof/ytdl-flask:v${BUILD_NUMBER} .
				echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin
				docker push ilyatrof/ytdl-flask:v${BUILD_NUMBER}
				'''
            }
        }
        stage('Deploy') {
            steps {
				script {
                    try{
						def old_container_id_list = (sh(returnStdout: true, script: "docker --host $DOCKER_HOST ps -a | grep ilyatrof/ytdl-flask | awk '{ print \$1 }'")).replace("\n", " ")
						sh 'echo Try to kill cootainers'
						sh "docker --host $DOCKER_HOST kill $old_container_id_list"
                    }catch (err) {
                        sh 'echo Kill older cootainers ERROR'
                    }
                    try{
						def old_images_id_list = (sh(returnStdout: true, script: "docker --host $DOCKER_HOST images | grep ilyatrof/ytdl-flask | awk '{ print \$3 }'")).replace("\n", " ")
						sh 'echo Try to remove image'
						sh "docker --host $DOCKER_HOST rmi -f $old_images_id_list"
					}catch (err) {
                        sh 'echo Remove older image ERROR'
                    }
                }
                sh 'echo Deploy new container'
                sh 'docker --host $DOCKER_HOST run --rm --name ytdl-flask-app -d -p 5000:5000 ilyatrof/ytdl-flask:v${BUILD_NUMBER}'
            }
        }
		stage('Clearing') {
            steps {
				script {
					def build_images_id_list = (sh(returnStdout: true, script: "docker images | grep ilyatrof/ytdl-flask | awk '{ print \$3 }'")).replace("\n", " ")
					if (build_images_id_list) {
						sh """
						echo Clearing after build
						docker ps
						docker ps -a
						docker rmi -f $build_images_id_list
						"""
					}
				}
			}
		}
	}
}