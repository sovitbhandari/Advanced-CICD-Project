pipeline {
  agent any
  environment {
    DOCKER_USER = credentials('dockerhub-user')     
    DOCKER_PASS = credentials('dockerhub-pass')    
    IMAGE_NAME  = "${DOCKER_USER}/python-cicd-app:${env.BUILD_NUMBER}"
    SONAR_TOKEN = credentials('sonar-token')
  }
  stages {
    stage('Checkout') {
      steps { git url: 'https://github.com/sovitbhandari/Advanced-CICD-Project.git', branch: 'main' }
    }
    stage('Unit Tests') {
      steps {
        sh '''
          python -m venv venv && . venv/bin/activate
          pip install -r app/requirements.txt pytest coverage
          coverage run -m pytest -q && coverage xml
        '''
      }
    }
    stage('Static Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh 'sonar-scanner -Dsonar.login=$SONAR_TOKEN'
        }
      }
    }
    stage('Build & Push Docker') {
      steps {
        script {
          sh "docker build -t ${IMAGE_NAME} ."
          sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
          sh "docker push ${IMAGE_NAME}"
        }
      }
    }
    stage('Patch Manifests → Git') {
      steps {
        sh """
          sed -i.bak 's|replaceImageTag|${BUILD_NUMBER}|' kubernetes/deployment.yaml
          git config user.email "jenkins@local" && git config user.name "jenkins"
          git add kubernetes/deployment.yaml
          git commit -m "CI: update image tag to ${BUILD_NUMBER}"
          git push origin main
        """
      }
    }
  }
}
