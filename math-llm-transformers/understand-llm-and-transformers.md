# BERT Model vs DistilBERT Model

### 1. Architecture
- The Bert-based model has 12 transformer layers (Also called encoder layers), 12 attention heads and a hidden size of 766(embedding dimensions). This results in the model of approximately 110 million parameters.
- The DistilBert-based model has 6 transformer layers, 12 attention heads and a hidden size of 768. This results in the model with approximately 66 million parameters. Whcih is roughly 40% smaller than BERT-Based model

### 2. Efficiency (Speed, memory, performance...)
- The BERT-base require more computational resources and time for both training and inference, due to its large size.
- The DistilBERT-based model is 60% faster than BERT-based during inference because of its reduced size and fewer transformer layers.
- The BERT-based also consumes more RAM memory during training due to the lager number of parameters.
- DistilBERT requires significantly less memory, making it more suitable for deployment on devices with limited resources(ex: mobile devices).

### 3. Summary
- The DistilBERT-based model is 40% smaller and retains 90% of BERTs performance.
- So, There is a tiny trade-off when it comes to accuracy, but a huge gain when it comes to deployment because it's smaller and faster.
- Therfore, for 95% of the NLP(Natural Language Processing) tasks that you are going to be doing, The DistilBERT-based is going to be enough.
- Advice: Use BERT-Base for specialized, data-heavy tasks where precision is more critical than speed—especially when the model needs to capture intricate relationships within the text.

![architecture](img/training-architecture.png)


# Embeddings

### 1. Definition
Embedding is a way to represent tokens as vectors of a continuous vector space or numerical space. This allows words with similar meanings to have similar representation. That will make it easy for model to understand the relationship between these two meanings.(Translates words into a language that computers can understand and process).

![Embedding](img/embedding.png)

### 2. Very simple embeddings representation
This is a 3 dimension(3D) representation that is very very simple, just to understand.\
Real life Distilled BERT models are 768 dimensions(768D).

![Embedding](img/embeddings.png)

In BERT & DistilBERT architectures, the embedding layer is the very first layer of the model.


# Positional Encodings 

### Why ?
Unlike RNN-based Encoder(type of Neural Network architecture used in NLP before the "Transformer" era which gave us BERT) which looks at sentence sequencially After embeddings, Transformer's Encoder looks at the entire sequence at once and can't know tokens order.

![Embedding](img/RNN-vs-Transformer.png)

In order for the model to understand the correct position of the words, we need to add the so-called **Positional Encodings** so that the model will know the words order.

![Embedding](img/positional-encodings.png)


# Attention Mechanism

### 1. Self attention
**Self attention** allows the model to understand the meaning of one word in a sentence.\
In the sentense : `[CLS] The bank of the river was flooded [SEP]` The word `bank` does not mean a financial institution.\
Self attention compare/Calculate(With math) de relation between the word bank and other words in the sentence to get its real meaning in that sentence. 

### 2. How does Self Attention works ?
#### Step 1
Each embedded vector(Each embedded word token) will be multiplied by:\
`Query` Metrics to get a **Query vector**\
`Key` Metrics to get a **Key vector**\
`Value` Metrics to get a **Value vector**

![Embedding](img/linear-transformation.png)

So, after the linear transformation, we are going to have :\
As many Query vectors as we have words in the input sentence.\
As many Key vectors as we have words in the input sentence.\
As many Value vectors as we have words in the input sentence.

#### Step 2