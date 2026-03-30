pipeline {
    agent none

    stages {

        stage('Build Docker Image') {
            agent { label 'docker' }
            steps {

                sh '''
                    docker build -t book-service:latest .
                '''

            }
        }

        stage('Trivy scan') {
            agent { label 'docker' }
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:0.69.3 \
                        image \
                        --severity CRITICAL,HIGH \
                        --ignore-unfixed \
                        --exit-code 1 \
                        --pkg-types os,library \
                        --no-progress \
                        --show-suppressed \
                        book-service:latest
                '''
            }
        }

        stage('Push image to docker registry') {
            agent { label 'docker' }
            steps {

                sh '''
                    docker tag book-service:latest 192.168.1.10:5000/library/book-service:latest
                    docker push 192.168.1.10:5000/library/book-service:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'kubectl' }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl --context kind-library apply -f deployment.yml
                        kubectl --context kind-library apply -f service.yml
                        kubectl --context kind-library rollout status deployment/book-service
                    '''
                }
            }
        }
    }
}