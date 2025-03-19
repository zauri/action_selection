## Model evaluation

### Folders
- cpt: Compact Prediction Tree
    - data: Input data
    - results: CPT output
- neural net: Neural networks (RNN + Feed-forward NN)
    - archive: Old versions
    - data: Input data
    - figures: Generated plots, overview of network architecture, ...
    - models: Saved (trained) models
    - results: Output data
    - tutorials: Tutorials for LSTM, RNN with GRU, and a text prediction neural net.

### Files
- cpt: Implementation of a compact prediction tree. 

- neural net
    - *nn\_with\_spatial\_info\**: Implementation of a feed-forward neural network for action selection prediction of different everyday activities.
    - *pytorch\_gru\_prequential\**: Implementation of a recurrent neural network doing text prediction on action sequences.