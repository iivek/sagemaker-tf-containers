## TensorFlow Serving container for AWS SageMaker

###Overview

Building on [a good read by Márcio Dos Santos](https://medium.com/ml-bytes/how-to-create-a-tensorflow-serving-container-for-aws-sagemaker-4853842c9751),
the repository facilitates containerization of Tensorflow server
containers for SageMaker and is by itself a container.

###Usage

Build docker image
```
git clone https://github.com/iivek/sagemaker-tf-containers.git
cd sagemaker-tf-containers && docker build -t sagemaker-tf .
```

Create model serving container from `sagemaker-tf-containers/models/<your-saved-model>`
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $PWD/models_works:/app/models sagemaker-tf \
-model_name <your_saved_model> -version <version> -docker_name <docker_name>
```

Run the server image
```
`cd <your_saved_model> && sh docker_run.sh`
```
