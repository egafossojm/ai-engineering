# Deploy a model using Sagemaker

## Prerequisites
- AWS account
- Amazon sagemaker domain with an active user profile (see [configuration steps](https://github.com/egafossojm/ai-engineering/blob/main/amazon-sagemaker/domain-setup.md))

## 1. Via AWS Console
1. Open **Amazon SageMaker AI** and navigate to the domains tab. 
2. Hit `open studio` in front of your domain, and select the user profile you want to use and open SageMaker Studio.
3. Select `JupyterLab` in the **Applications** frame and run the JupyterLab space you want if any. If not space, create one with default config and launch it.
4. Check the space **Status** and **Action** columns to make sure the space is ready, Then `Open` it.
5. Once in the JupyterLab Launcher, create a Notebook (`File` > `New` > `Notebook`).
6. Navigate to [Hugging Face website](https://huggingface.co/models) to get a free model.
7. Once on the models page, use the search bar to find and select a specific model or type of models.\
![Select a Hugging face model](img/select-hugging-face-model.png)
8. On the choosen model page, you can test the model with the **Inference Providers** pn the right hand side.\
![inference providers](img/inference-providers.png)
9. On the top right of the model page, click `Deploy` button and select `Amazon SageMaker`.
10. copy the **deploy.py** file and paste it in JupyterLab Notebook. 
```python
# WARNING: This snippet is not yet compatible with SageMaker version >= 3.0.0.
# To use this snippet, install a compatible version:
# pip install 'sagemaker<3.0.0'
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

try:
	role = sagemaker.get_execution_role()
except ValueError:
	iam = boto3.client('iam')
	role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'cardiffnlp/twitter-roberta-base-sentiment-latest',
	'HF_TASK':'text-classification'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	transformers_version='4.51.3',
	pytorch_version='2.6.0',
	py_version='py312',
	env=hub,
	role=role, 
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.g6.2xlarge' # ec2 instance type
)

predictor.predict({
	"inputs": "I like you. I love you",
})
```
11. In the notbook, Insert a cell at the first rank and type
```shell
pip install 'sagemaker<3.0.0
```
12. Make sure the notebook has the necessary packages used by the model.
```python
# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	transformers_version='4.51.3',
	pytorch_version='2.6.0',
	py_version='py312',
	env=hub,
	role=role, 
)
```
13. You can update the instances config to deploy model to SageMaker Inference
```pyhton
# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.g6.2xlarge' # ec2 instance type
)
```
12. Run All cells in the NoteBook to start prediction.

