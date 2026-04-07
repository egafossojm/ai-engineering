# BERT Model vs DistilBERT Model

### 1. Architecture
- The Bert-based model has 12 transformer layers (Also called encoder layers), 12 attention heads and a hidden size of 766. This results in the model of approximately 110 million parameters.
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
