### Google-Developer-Group-CV
<div align="center">
   
---
# AI-Powered Visual Sign Language Mastery Reimagined
## Teaching Hands to Talk, Pixels to Listen

</div>

An interactive American Sign Language (ASL) learning platform that uses computer vision and deep learning to provide real-time feedback on ASL gestures. The system employs Convolutional Neural Networks to recognize ASL letters (A-Z) and numbers (0-9).

## Important Notes
Before adding or committing changes, ensure that `.gitignore` excludes your virtual environment folder to avoid pushing dependencies.

## Requirements
Use a virtual environment when running the program. To create a virtual environment, follow the steps:
1. Create environment
   1. `python -m venv [name]`
2. Activate the environment
   1. `source [name]/bin/activate`
3. Install the requirements
   1. `pip install -r requirements.txt`

To deactivate the virtual environment, simply run: `deactivate`

## Project Components

### Model Architecture
- Input: 64x64 RGB images
- Three convolutional layers with batch normalization
- Dropout layers for regularization
- Dense layers with sigmoid activation for binary classification
- Individual classifiers for each ASL letter and number

### Dataset

The model uses the ASL Dataset from Kaggle. To use this code:

1. Set up your Kaggle API credentials
2. The dataset will be automatically downloaded and unzipped
3. Images should be organized in folders by letter/number

### Dataset Structure
```
asl_dataset/
├── a/                  # Images for letter 'A'
├── b/                  # Images for letter 'B'
...
├── z/                  # Images for letter 'Z'
├── 0/                  # Images for number '0'
...
└── 9/                  # Images for number '9'
```

### Training Process
- Binary classification approach
- Data augmentation with rotation and scaling
- 80-20 train-validation split
- Early stopping and learning rate reduction
- Separate models for each letter/number

### Save Format
Trained models are saved in the 'model_serialization' directory with the naming convention:
```bash
asl_model_[letter/number].keras
```

## Running the Camera
To test the camera file, follow the instructions from the requirements section to set up the environment. After doing so, you can run the camera file in the virtual environment:
```bash
python camera.py
```

## Implementation Details

### Model Training
```python
classifier = ASLBinaryClassifier(letter='A')
classifier.prepare_data()
classifier.build_model()
classifier.train()
```

### Dependencies
- TensorFlow
- OpenCV
- Keras
- NumPy
- Matplotlib

## Future Development
- Web application interface
- Interactive learning exercises
- Progress tracking
- Performance analytics

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome. Please fork the repository and submit pull requests to contribute.

## Acknowledgments
- [ASL Dataset from Kaggle](https://www.kaggle.com/datasets/ayuraj/asl-dataset)
- [Google Developer Group](https://gdg.community.dev/gdg-on-campus-new-york-university-new-york-united-states/)
