import yaml
import json
import uuid
import os

def generate_uuid():
    """生成UUID并返回字符串形式"""
    return str(uuid.uuid4())

def convert_yaml_to_json(yaml_path, json_path):
    """将YAML文件转换为JSON文件，并为每个资源添加UUID"""
    # 读取YAML文件
    with open(yaml_path, 'r', encoding='utf-8') as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    # 尝试读取现有的JSON文件，获取已有的UUID
    existing_uuids = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
                if 'resources' in existing_data:
                    for resource in existing_data['resources']:
                        if 'name' in resource and 'uuid' in resource:
                            existing_uuids[resource['name']] = resource['uuid']
        except Exception as e:
            print(f"读取现有JSON文件时出错: {e}")
    
    # 为每个资源添加UUID，优先使用已有的
    if 'resources' in data:
        for resource in data['resources']:
            # 如果资源在现有JSON中有UUID，则使用已有的UUID
            if 'name' in resource and resource['name'] in existing_uuids:
                resource['uuid'] = existing_uuids[resource['name']]
            # 否则，如果资源没有UUID，则生成新的
            elif 'uuid' not in resource:
                resource['uuid'] = generate_uuid()
    
    # 写入JSON文件
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"转换完成: {yaml_path} -> {json_path}")

if __name__ == "__main__":
    # 设置文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(script_dir, "info.yaml")
    json_path = os.path.join(script_dir, "metadata.json")
    
    # 执行转换
    convert_yaml_to_json(yaml_path, json_path)
