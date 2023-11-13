import os
import subprocess

# 'fonts' 디렉토리 내의 모든 하위 디렉토리 가져오기
font_dirs = [d for d in os.listdir("fonts") if os.path.isdir(os.path.join("fonts", d))]

# 명령 실행 및 labels-map.csv 파일 병합을 위한 준비
all_labels = []

for font_dir in font_dirs:
    image_data_dir = os.path.abspath(f"./image-data/{font_dir}")
    if not os.path.exists(image_data_dir):
        os.makedirs(image_data_dir)

    # 이미지 생성 명령 실행
    command = f"python tools/hangul-image-generator.py --label-file ./labels/256-common-hangul.txt --font-dir ./fonts/{font_dir} --output-dir {image_data_dir}"
    subprocess.run(command, shell=True, stderr=subprocess.DEVNULL)  # 에러 메시지 무시

    # labels-map.csv 파일 읽기
    labels_map_file = os.path.join(image_data_dir, "labels-map.csv")
    if os.path.exists(labels_map_file):
        try:
            with open(labels_map_file, 'r', encoding='utf-8') as file:
                all_labels.extend(file.readlines())
        except UnicodeDecodeError as e:
            print(f"Error reading {labels_map_file}: {e}")

# 모든 labels-map.csv 내용을 하나의 파일로 병합
with open("./image-data/labels-map.csv", 'w', encoding='utf-8') as merged_file:
    merged_file.writelines(all_labels)
