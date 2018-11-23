#!/usr/bin/env groovy

def copyTitoBuildProducts() {
    sh '''
        pwd
        ls -la . /tmp/tito || :
        mkdir -p rpmbuild/SRPMS
        cp -p /tmp/tito/*.src.rpm rpmbuild/SRPMS
        mkdir -p rpmbuild/RPMS/noarch
        cp -p /tmp/tito/noarch/*.rpm rpmbuild/RPMS/noarch
        ls -la . /tmp/tito
    '''
}

pipeline {
    agent {
        docker { 
            image 'centos-7-build:latest' 
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    stages {
        stage('test build') {
            when {
                not {
                    branch 'master'
                }
            }
            steps {
                sshagent(['2bbe635f-1041-4c65-8448-28c7680f1e33']) {
                    sh '''
                        id
                        pwd
                        ls -la . /tmp/tito || :
                        tito build --test --rpm
                        ls -la . /tmp/tito
                    '''
                }
            }
        }

        stage('build master') {
            when {
                branch 'master'
            }
            steps {
                sshagent(['2bbe635f-1041-4c65-8448-28c7680f1e33']) {
                    sh '''
                        tito build
                    '''
                }
            }
        }

        stage('release') {
            steps {
                sshagent(['2bbe635f-1041-4c65-8448-28c7680f1e33']) {
                    copyTitoBuildProducts()
                }
            }
        }
    }
}
