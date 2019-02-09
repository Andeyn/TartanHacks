from imageai.Detection import ObjectDetection
import os

def detectObj():
    execution_path = os.getcwd()

    detector = ObjectDetection()    
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "OBAMA.jpg"),    output_image_path=os.path.join(execution_path , "andeyrequest'.jpg"))
    result = []

    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        result.append(eachObject["name"])
    
    return result
    