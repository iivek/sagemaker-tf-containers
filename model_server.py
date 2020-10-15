import tensorflow as tf
from tensorflow.keras.models import load_model
from shutil import copyfile
import os
import argparse



def serialized_to_savedmodel(serialized, destination):
    """
    Re-saves a serialized (h5, hdf5) model as SavedModel

    :param serialized: filename, serialized model
    :param destination:
    :return:
    """

    # TODO: try to fix saving of the entire model - otherwise we'll need
    # to keep track of model architecture

    model = load_model(serialized)

    # https://www.tensorflow.org/tfx/tutorials/serving/rest_simple
    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None
    )

    return destination


def docker_build_automation(model_name,
                            version,
                            docker_name,
                            model_path,
                            dockerfile_template='./Dockerfile.template',
                            nginx_conf_template = './nginx.conf.template'
                            ):
    """
    Prepares the dockerfile and moves it to the location where SerializedModel is stored.
    Builds the image. Outputs the corresponding docker run command.
    In the image, the endpoints are reverse proxied to match SageMaker's conventions (see references)

    [0] https://medium.com/ml-bytes/how-to-create-a-tensorflow-serving-container-for-aws-sagemaker-4853842c9751
    [1] https://github.com/aws/amazon-sagemaker-examples/blob/master/advanced_functionality/tensorflow_bring_your_own/tensorflow_bring_your_own.ipynb
    
    :param model_name: 2nd level directory name in Tensorflow's SavedModel directory structure
    :param version: maps to tf server URL endpoint
    :param docker_name: name of the docker image containing the sever
    :param model_path:
    :param dockerfile_template='./Dockerfile.template',
    :param nginx_conf_template = './nginx.conf.template'
    
    
    :param dockerfile:
    :return: docker build command, docker run command
    """

    # copy the dockerfile_templage and nginx templates
    copyfile(dockerfile_template, os.path.join(model_path, 'Dockerfile'))
    nginx_dest = os.path.join(model_path, 'nginx.conf')
    copyfile(nginx_conf_template, nginx_dest)

    return ("docker build"           
            " --build-arg MODELNAME_ARG={model_name}"
            " -t {docker_name} .".format(**locals()),
            "docker run --rm -p 8080:8080"
            " {docker_name}".format(**locals())
            )


if __name__ == '__main__':    
    import sys    

    parser = argparse.ArgumentParser()
    parser.add_argument('-model_path')
    parser.add_argument('-version')
    parser.add_argument('-model_name')
    parser.add_argument('-docker_name')
    print(parser)
    arg_dict = vars(parser.parse_args())
    print(arg_dict)
        
    docker_commands = docker_build_automation(**arg_dict)
    # save the command to build the image...
    with open(arg_dict['model_path'] + "/docker_build.sh", 'w') as file:
        file.write(docker_commands[0])
    # ... and the command to run the image
    with open(arg_dict['model_path'] + "/docker_run.sh", 'w') as file:
        file.write(docker_commands[1])
