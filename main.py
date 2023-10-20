import cv2
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image

# Load the processor and model
processor = DetrImageProcessor.from_pretrained("")
model = DetrForObjectDetection.from_pretrained("")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
    
    pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Process the frame
    inputs = processor(images=pil_frame, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([pil_frame.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        if label == 3:  
            print('carro detectado!!!!')
            box = [round(i, 2) for i in box.tolist()]
            x, y, xmax, ymax = box
            cv2.rectangle(frame, (int(x), int(y)), (int(xmax), int(ymax)), (255, 0, 0), 2)
            cv2.putText(frame, "CARRO ENCONTRADO UHUL o/", (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imshow('Detected Car', frame)

    cv2.imshow('Webcam Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
