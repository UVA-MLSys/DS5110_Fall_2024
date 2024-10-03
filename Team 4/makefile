default:
	echo @ makefile

build_venv:
	pip install --upgrade pip;
	python3.11 -m venv .venv;
	source .venv/bin/activate && pip install -r requirements.txt;

install_kernel: .venv
	source .venv/bin/activate && python3.11 -m ipykernel kernel --user --name .venv --display-name = "Python (3.11 .venv)"

.PHONY: tests
tests: update 
	source .venv/bin/activate; pytest -vvx tests/

# may need to be logged into Kaggle
# url if this doesn't work https://www.kaggle.com/datasets/aaron7sun/stocknews
# is there anything in this SHA that would be unsafe?
download_data:
	wget https://storage.googleapis.com/kaggle-data-sets/129/792900/bundle/archive.zip\?X-Goog-Algorithm\=GOOG4-RSA-SHA256\&X-Goog-Credential\=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20241003%2Fauto%2Fstorage%2Fgoog4_request\&X-Goog-Date\=20241003T150846Z\&X-Goog-Expires\=259200\&X-Goog-SignedHeaders\=host\&X-Goog-Signature\=996c377cf08a69ca47deae453fc34dbdf6c5307f06984183943e716013f71f73994b2b9ad5d706ed7cd063763b5f0f14bb5e30214cacc909d72cfa145295ccb2ed260ef79eaa7d55cfa827b0b4ff34b6f19a9e98045910b29e9f7d206267beaa73dbd877ef4e04a6079763d8091c33cdb9f39152b369be1b9b8989780f319e08336549d847ad42a9b834b044bc4c00c43f0b368b3b8029d31d7c765b93693ddeddecd0a03139a35f88aafa8abf691c03abc265c400b299946ffe3b7f28d7b0d5d2c289ed24ebf84c2b345ae750979478672c99993423b6714db81435f53854633089ce9dc03eaf29140a0f3fd1267dd13b1d904d4e45f36ee3572e7ed96d74a1 -O data/raw/stock_reddit_data.zip;
	unzip data/raw/stock_reddit_data.zip -d data/raw/stock_reddit_data
	rm -rf data/raw/stock_reddit_data.zip

# do something with the data


# TODO: connect to aws
# connect to aws


# things you might need on an aws server
# wget unzip make