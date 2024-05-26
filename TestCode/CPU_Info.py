import GPUtil


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_list = []

    for gpu in gpus:
        gpu_info = {
            'id': gpu.id,
            'name': gpu.name,
            'driver_version': gpu.driver,
            'memory_total': gpu.memoryTotal,
            'memory_used': gpu.memoryUsed,
            'memory_free': gpu.memoryFree,
            'temperature': gpu.temperature,
            'load': gpu.load * 100,
            'uuid': gpu.uuid
        }
        gpu_list.append(gpu_info)

    return gpu_list


gpu_info = get_gpu_info()

for info in gpu_info:
    print(f"ID: {info['id']}")
    print(f"Name: {info['name']}")
    print(f"Driver Version: {info['driver_version']}")
    print(f"Total Memory: {info['memory_total']} MB")
    print(f"Used Memory: {info['memory_used']} MB")
    print(f"Free Memory: {info['memory_free']} MB")
    print(f"Temperature: {info['temperature']} C")
    print(f"Load: {info['load']} %")
    print(f"UUID: {info['uuid']}")
    print("=" * 30)