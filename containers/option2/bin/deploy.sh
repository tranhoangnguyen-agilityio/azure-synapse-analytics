#!/bin/bash

# Please setup the following env variables:
# - SYNAPSE_GIT_REPO: The tenant git repository. E.g: git@github.com:example-group/example-repo-name.git
# - AZURE_KEY_VAULT: Tenant azure key value name
# - AZURE_SECRET_NAME: The secret key name inside the AZURE_KEY_VAULT that contains the Github deploykey
# - CONTAINER_IDENITY_PRINCIPAL_ID: The identity principal id for this container

echo GITHUB_ACCOUNT=$GITHUB_ACCOUNT
echo REPOSITORY_NAME=$REPOSITORY_NAME
echo COLLABORATION_BRANCH=$COLLABORATION_BRANCH
echo SYNAPSE_GIT_REPO=$SYNAPSE_GIT_REPO
echo AZURE_KEY_VAULT=$AZURE_KEY_VAULT
echo AZURE_SECRET_NAME=$AZURE_SECRET_NAME
echo CONTAINER_IDENITY_PRINCIPAL_ID=$CONTAINER_IDENITY_PRINCIPAL_ID

SYNAPSE_GIT_REPO='git@github.com:'$GITHUB_ACCOUNT'/'$REPOSITORY_NAME'.git'
GITHUB_DEPLOYKEY_PATH=$PWD/$AZURE_SECRET_NAME
echo GITHUB_DEPLOYKEY_PATH=$GITHUB_DEPLOYKEY_PATH


# Download the deploy key
az login --identity --username $CONTAINER_IDENITY_PRINCIPAL_ID
az keyvault secret download --file $GITHUB_DEPLOYKEY_PATH --vault-name $AZURE_KEY_VAULT --name $AZURE_SECRET_NAME
chmod 600 $GITHUB_DEPLOYKEY_PATH

cd option2/src
ls

# Init git
git init
git config user.email "tran.hoangnguyen@asnet.com.vn"
git config user.name "Tran Hoang"
git remote add upstream $SYNAPSE_GIT_REPO

# Commit
git checkout -b $COLLABORATION_BRANCH
git add .
git commit -a -m "autoupdate `date +%F-%T`"

# Push
GIT_SSH_COMMAND='ssh -i '$GITHUB_DEPLOYKEY_PATH' -o IdentitiesOnly=yes -F /dev/null' git push upstream $COLLABORATION_BRANCH
echo 'Push code to tenant github.'

# Remove key
rm $GITHUB_DEPLOYKEY_PATH
echo 'The deploy key is deleted.'

# az keyvault secret download --file secretkey --vault-name tenant-github-deploykey --name deploykey