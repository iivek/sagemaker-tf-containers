# TensorFlow Serving containers for AWS SageMaker

## Overview

Building on [a good read by Márcio Dos Santos](https://medium.com/ml-bytes/how-to-create-a-tensorflow-serving-container-for-aws-sagemaker-4853842c9751),
the repository facilitates containerization of TensorFlow Serving for SageMaker and is by itself a container.

## Usage

Build docker image
```
git clone https://github.com/iivek/sagemaker-tf-containers.git
cd sagemaker-tf-containers && docker build -t sagemaker-tf .
```

Run docker image to create serving image from the model in `sagemaker-tf-containers/models/<your-saved-model>`
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $PWD/models_works:/app/models sagemaker-tf \
-model_name <your_saved_model> -version <version> -docker_name <docker_name>
```


## Example
We'll build serving image from [saved_model_half_plus_two](https://www.tensorflow.org/tfx/serving/docker) demo model.

Let's download the servable to `sagemaker-tf-containers/models/`
```
mkdir models
git clone https://github.com/tensorflow/serving /tmp/serving && \
cp -r /tmp/serving/tensorflow_serving/servables/tensorflow/testdata/saved_model_half_plus_three ./models
```
Running the `sagemaker-tf` container to build server image named `half_plus_two_servable` 
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $PWD/models:/app/models sagemaker-tf \
-model_name saved_model_half_plus_three -version 0.9 -docker_name half_plus_two_server
```
Notice that the invocation needs to bind sockets of our Docker host to the sockets of Docker-within-Docker that actually builds the
serving image.

To locally test the serving image, let's run it
```
docker run --rm -p 8080:8080 half_plus_two_server
```
and send a request to get predictions
```
$ curl -X POST http://localhost:8080/invocations -d '{"instances": [1.0,2.0,5.0]}'   
{
    "predictions": [3.5, 4.0, 5.5
    ]
}
```
