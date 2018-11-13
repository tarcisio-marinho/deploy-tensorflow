# Deploy a tensorflow on production


**Tensorflow serving** - handles all the infaestructure of models on a webserver
    model management
    version management
    inference
    C++

    gRPC protocol - over HTTP
        only GET and POST methods


build ment to be on production by google 

# INSTALLATION

**Install docker** -> https://docs.docker.com/install/
        '''
        $ sudo apt-get update

        $ sudo apt-get install \
            apt-transport-https \
            ca-certificates \
            curl \
            gnupg2 \
            software-properties-common


        $ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
        
        $ sudo add-apt-repository \
            "deb [arch=amd64] https://download.docker.com/linux/debian \
            jessie \
            stable"

        $ sudo apt-get update

        $ sudo apt-get install docker-ce

        # check if installation went well
            $ sudo docker run hello-world
        '''
**Install git**

        $ sudo apt-get install git

**Download tensorflow serving**
    
    $ git clone --recursive https://github.com/tensorflow/serving

**Downloading dependencies**

    $ cd serving/

    $ sudo docker build --pull -t $USER/tensorflow-serving-devel -f tensorflow_serving/tools/docker/Dockerfile.devel .

**Run Docker**

    $ sudo docker run --name=tensorflow_container -it $USER/tensorflow-serving-devel

**Inside the docker**

    $ cd /tensorflow-serving/
    $ bazel build -c opt tensorflow_serving/...


