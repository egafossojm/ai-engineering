# Amazon SageMaker Domain Setup

## Prerequisites

- AWS Account
- IAM user with needed permissions or with adminstrators permissions to make things simple

### Via AWS Console
1. Go to the Amazon SageMaker console
2. Under the **Environment configuration**, in the **Domains** tab, click on `Create domain`
3. Select `Set up for single user (Quick setup)` and click on `Set up`
4. If no default user is created with the domain, go to domain page, under **User profiles** and create one. Go with default configs.
5. Once created, Go to your domain page, under **User profiles**, next to your created user, hit `Open Studio`.


## Compute
- We will use `ml.t3.medium` to setup things.(We just need CPU).
- We will use **Accelerated Computing**(`ml.p2.xlarge`) instances for training (any `xx.px.xxxxxx`has GPU).
- [Pricing](https://aws.amazon.com/sagemaker/ai/pricing/)