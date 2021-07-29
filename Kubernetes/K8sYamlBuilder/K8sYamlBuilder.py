import json
import os
from pprint import pprint

K8s_YAML_BUILDER_PATH = os.path.dirname(os.path.abspath(__file__))

SIDECAR_TEMPLATE = "- name: %s-pod\n          image: %s"

# Add params to work_model json
# http://s1.default.svc.cluster.local
def customization_work_model(model, k8s_parameters):
    for service in model:
        model[service].update({"url": f"{service}.{k8s_parameters['namespace']}.svc.{k8s_parameters['cluster_domain']}.local"})
        model[service].update({"path": k8s_parameters['path']})
        model[service].update({"image": k8s_parameters['image']})
        model[service].update({"namespace": k8s_parameters['namespace']})
    print("Work Model Updated!")


def create_deployment_yaml_files(model, k8s_parameters, nfs, output_path):
    namespace = k8s_parameters['namespace']
    for service in model:
        with open(f"{K8s_YAML_BUILDER_PATH}/Templates/DeploymentTemplate.yaml", "r") as file:
            f = file.read()
            f = f.replace("{{SERVICE_NAME}}", service)
            f = f.replace("{{IMAGE}}", model[service]["image"])
            f = f.replace("{{NAMESPACE}}", namespace)
            if "sidecar" in model[service].keys():
                f = f.replace("{{SIDECAR}}", SIDECAR_TEMPLATE % (model[service]["sidecar"], model[service]["sidecar"]))
            else:
                f = f.replace("{{SIDECAR}}", "")

        if not os.path.exists(f"{output_path}/yamls"):
            os.makedirs(f"{output_path}/yamls")

        with open(f"{output_path}/yamls/{k8s_parameters['prefix_yaml_file']}-{service}.yaml", "w") as file:
            file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/ConfigMapNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)
        f = f.replace("{{PATH}}", k8s_parameters["path"])

    with open(f"{output_path}/yamls/ConfigMapNginxGw.yaml", "w") as file:
        file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/DeploymentNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)

    with open(f"{output_path}/yamls/DeploymentNginxGw.yaml", "w") as file:
        file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/PersistentVolumeMicroServiceTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)
        f = f.replace("{{SERVER}}", nfs["address"])
        f = f.replace("{{PATH}}", nfs["mount_path"])

    with open(f"{output_path}/yamls/PersistentVolumeMicroService.yaml", "w") as file:
        file.write(f)

    print("Deployment Created!")


def create_configmap_yaml(mesh, model, namespace, output_path):
    with open(f"{K8s_YAML_BUILDER_PATH}/Templates/ConfigMapTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{SERVICE_MESH}}", json.dumps(mesh))
        f = f.replace("{{WORK_MODEL}}", json.dumps(model))
        f = f.replace("{{NAMESPACE}}", namespace)

    if not os.path.exists("yamls"):
        os.makedirs("yamls")

    with open(f"{output_path}/yamls/ConfigMapMicroService.yaml", "w") as file:
        file.write(f)

    print("ConfigMap Created!")
