
def Detection(fileName): #на вход изображение, на выходе список найденных дифектов
    from ultralytics import YOLO

    model = YOLO('Thebest.pt')

    class_name = model.names

    results = model.predict(source=fileName)
    AraryOfType = []
    ArrayOfBounds = {i:[] for key,i in class_name.items()}
    i=0
    for result in results:
        AraryOfType.append(len(results[i].boxes.conf.cpu().numpy())!=0)
        i+=1

    for i in range(len(AraryOfType)):
        if(AraryOfType[i]):
            for data in results[i].boxes.data.tolist():
                temp = []

                print(data)
                xmin, ymin, xmax, ymax, confidence ,class_id= data

                xmin = int(xmin)
                ymin = int(ymin)
                xmax = int(xmax)
                ymax = int(ymax)
                temp.append(xmin)
                temp.append(ymin)
                temp.append(xmax)
                temp.append(ymax)

                ArrayOfBounds[class_name[int(class_id)]].append(temp)

    return(ArrayOfBounds)


