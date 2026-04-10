# Understanding of Python libraries used in our fine-tuning project

### Pandas
For data processing (data loading and structural manipulation).

### Transformers
transformers is the HuggingFace library that provides:
- pretrained models
- tokenizers
- pipelines
- utilities for NLP, vision, audio, and multimodal tasks

It includes dozens of model families(`Architectures`):
- BERT
- DistilBERT (Same architecture as BERT but only 6 transformer layers)
- RoBERTa
- GPT‑2
- T5
- DeBERTa
- etc.

### The PyTorch Training Pipeline: torch, Dataset, DataLoader

#### 1. torch — The core deep learning framework.

`torch` is the foundation of PyTorch.\
It provides:
- tensors (like NumPy arrays but on GPU)
- automatic differentiation (autograd)
- neural network layers (torch.nn)
- optimizers (torch.optim)
- GPU acceleration (CUDA)
- model training utilities

#### 2. Dataset — your data, wrapped in a PyTorch‑friendly class

A `Dataset` is a Python class that tells PyTorch:
- how many samples you have (`__len__`)
- how to load one sample (`__getitem__`)

You created this:
```python
class NewsDataset(Dataset):
    def __getitem__(self, index):
        # returns one training example
```
This class:
- reads your DataFrame
- tokenizes the text
- returns tensors (input_ids, attention_mask, label)

👉 Dataset = your data + your preprocessing logic

#### 3. DataLoader — batches, shuffling, multiprocessing
A DataLoader takes a Dataset and handles:
- batching
- shuffling
- parallel loading (via num_workers)
- moving data to the model efficiently

```python
training_set = NewsDataset(train_dataset,tokenizer,MAX_LEN)
train_parameters = {
    'batch_size': TRAIN_BATCH_SIZE,
    'shuffle': True, data
    'num_workers': 0
}

training_loader = DataLoader(training_set,  **train_parameters)
```

This means:
- PyTorch will call your `Dataset.__getitem__` 4 times per batch
- It will shuffle the dataset each epoch
- It will return batches like:
```python
{
  "ids": tensor([...]),
  "mask": tensor([...]),
  "targets": tensor([...])
}
```
👉 DataLoader = efficient batching + shuffling + iteration

#### 4. How they work together during training
Here's the full flow:

```
Your CSV / DataFrame
        ↓
   Dataset (tokenization, labels)
        ↓
   DataLoader (batching, shuffle)
        ↓
   Model (DistilBERT)
        ↓
   Loss + Optimizer
```

**Step by step:**

a. Dataset  
Defines how to load and preprocess one sample.

b. DataLoader  
Groups samples into batches and feeds them to the model.

c. Model  
Receives tensors from the DataLoader and produces predictions.

d. Loss function  
Compares predictions to labels.

e. Optimizer  
Updates model weights.

**This loop repeats for every epoch.**


# DistilBERT Model + classifier
## Understanding the Model

```python
# defines a text classification model built on top of DistilBERT, with a custom neural network head.
class DistilBERTClass(torch.nn.Module):

    def __init__(self):
        super(DistilBERTClass, self).__init__()
        self.l1 = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(768, 4)

    def forward(self, input_ids, attention_mask):
         [...]
```

### 1. Base Transformer Encoder (DistilBERT)
```python
self.l1 = DistilBertModel.from_pretrained('distilbert-base-uncased')
```
This loads:
- The Transformer encoder architecture
- Pretrained weights (trained on massive corpora)
- Token embeddings
- Positional embeddings
- 6 Transformer layers (DistilBERT = compressed BERT)

DistilBERT outputs:
```
last_hidden_state → [batch_size, seq_len, 768]
```
Each token is represented by a 768‑dimensional contextual embedding.

This is the feature extractor of your model.

### 2. Pre‑classifier Linear Layer
```python
self.pre_classifier = torch.nn.Linear(768, 768)
```
This layer:
- Takes the CLS embedding (768 dims)
- Transforms it into another 768‑dimensional vector
- Helps the classifier learn richer features

Why keep the same dimension?
- It preserves the representational power of DistilBERT
- It allows the classifier to learn non‑linear transformations

### 3. Dropout Layer
```python
self.dropout = torch.nn.Dropout(0.3)
```
Dropout randomly zeros 30% of neurons during training.

Purpose:
- Reduce overfitting
- Force the model to learn robust features
- Improve generalization

### 4. Final Classification Layer
```python
self.classifier = torch.nn.Linear(768, 4)
```
This maps the 768‑dimensional sentence embedding to 4 logits, one per class.
Output shape:
```
[batch_size, 4]
```
These logits go into:
- `CrossEntropyLoss` during training
- `Softmax` during inference

## The Forward Pass

```python
class DistilBERTClass(torch.nn.Module):

    def __init__(self):
        [...]

    def forward(self, input_ids, attention_mask):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)

        return output
```

### 1. Pass Inputs Through DistilBERT
```python
output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
```
Inputs:
- `input_ids`: token IDs → [batch_size, seq_len]
- `attention_mask`: 1 for real tokens, 0 for padding → same shape

What DistilBERT does:
- embeds tokens
- adds positional encodings
- applies 6 Transformer layers
- computes contextual embeddings

Output:
`output_1[0]` = `last_hidden_state`
```
hidden_state shape = [batch_size, seq_len, 768]
```
This is a sequence of embeddings, one per token.

### 2. Extract the CLS Token Embedding
```python
hidden_state = output_1[0]
pooler = hidden_state[:, 0]
```
**Why token 0?**

In BERT‑style models:
- token 0 = [CLS]
- it is trained to represent the entire sentence
- it aggregates information from all tokens through self‑attention

Shape becomes:
```
pooler = [batch_size, 768]
```
This is now a sentence‑level embedding, not a sequence.

### 3. First Linear Layer (Feature Transformation)
```python
pooler = self.pre_classifier(pooler)
```

This applies:
```
Linear(768 → 768)
```
Purpose:
- Learn a better representation for classification
- Mix features
- Allow the classifier to learn non‑linear transformations

Shape stays:
```
[batch_size, 768]
```

### 4. Activation Function (ReLU)
```python
pooler = torch.nn.ReLU()(pooler)
```
ReLU introduces non-linearity, enabling the model to learn:
-Complex decision boundaries
- Non-linear relationships between features
- Without ReLU, your classifier would be almost linear.

### 5. Dropout (Regularization)
```python
pooler = self.dropout(pooler)
```
Dropout randomly zeros 30% of neurons.

Purpose:
- Prevent overfitting
- Force the model to rely on multiple features
- Improve generalization

Shape remains:
```
[batch_size, 768]
```

### 6. Final Classification Layer
```python
output = self.classifier(pooler)
```
This applies:
```
Linear(768 → 4)
```
Output shape:
```
[batch_size, 4]
```
These are raw logits, not probabilities.

### Full Forward Pass Summary (With Shapes)
```
input_ids:        [batch, seq_len]
attention_mask:   [batch, seq_len]
        ↓
DistilBERT encoder
        ↓
last_hidden_state: [batch, seq_len, 768]
        ↓
CLS token:         [batch, 768]
        ↓
Linear(768→768):   [batch, 768]
        ↓
ReLU:              [batch, 768]
        ↓
Dropout:           [batch, 768]
        ↓
Linear(768→4):     [batch, 4]
        ↓
logits
```

**Note: logits = raw Attentions scores(before softmax to convert in probabilities)**

They are Raw model outputs before softmax.

Shape example: `[batch_size, num_classes]`.

