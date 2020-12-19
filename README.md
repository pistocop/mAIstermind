# mAIstermind

> Project developed for a university exam in 2019

The aim of this project is to train and test differents sub-symbolic systems capable to play the mastermind board game. 
To do this, this repository contains: 
- Players that implement different mathematical strategies to play the game and build the training database 
- Neural networks implemented using Tensorflow Estimators 
- Jupyter notebooks to manage the databases 
- Jupyter notebooks to analyze the neural networks performances

## Changelog

### 2020 - Some notes
- This is my first ML project and the first "big" project in a more general sense
- I haven't changed anything from the exam submission, and I haven't plan to improve this package
- **Keypoints**
  - Mastermind players to build the dataset:
    - _knuth_ - best algorithm, from [Knuth paper](http://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf)
    - *knuth_fast* - my idea to speed-up knuth algorithm
    - *hopeful* - simple but fast algorithm
  - All the dataset are available on [mega](https://mega.nz/file/0tpQHCKI#4QoWmptACD2OYS4J_RXwJy13PWbBVFfVGZ3Oe4O74Is)
    - After unzip, those are the file:
    ```
    ❯ tree -s -h --du
    .
    ├── [ 99M]  hopeful
    │   ├── [ 69M]  hopeful.csv
    │   └── [ 30M]  hopeful_cuts.csv
    ├── [133K]  knuth
    │   ├── [ 89K]  knuth_optimal.csv
    │   └── [ 40K]  knuth_optimal_cuts.csv
    └── [ 19M]  knuth_fast
        ├── [5.8M]  knuth_cuts.csv
        └── [ 13M]  knuth_fast.csv

     118M used in 3 directories, 6 files
    ```
  - [Slides](/slides/Presentazione%20Mastermind.pdf) are available (in italian) for a deeper explanation of the project.
  - The trained models are 4 Bi-LSTM with attention System. They are written in Tensorflow using the [tf_estimator](https://www.tensorflow.org/api_docs/python/tf/estimator/Estimator).
