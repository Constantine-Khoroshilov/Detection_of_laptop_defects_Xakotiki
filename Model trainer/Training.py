from ultralytics import YOLO
import torch
# Загрузка модели YOLO (можете использовать yolov8n, yolov8s, yolov8m и т.д.)
model = YOLO('/content/yolo_training/yolo_experiment_1/weights/best.pt')  # YOLOv8n (Nano) — это легкая модель, хорошо подходит для небольших наборов данных

# Тренировка модели
model.train(
    data='data.yaml',  # Путь к конфигурационному файлу
    epochs=30,                # Количество эпох (можно начать с 50-100 эпох)
    batch=8,                  # Размер батча (оптимально для небольшого набора данных)
    imgsz=640,                 # Размер изображения
    workers=4,                 # Количество потоков для загрузки данных
    project='yolo_training',    # Папка, куда будут сохраняться результаты
    name='yolo_experiment_1',   # Название эксперимента
    device=0                   # Использование GPU (укажите "cpu" для процессора)
)

# Оценка модели на тестовом наборе данных
metrics = model.val(data='/content/data.yaml')  # Это оценит модель на валидационных данных