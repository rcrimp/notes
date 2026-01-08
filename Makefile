.DEFAULT_GOAL := serve

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

update-content:
	rm -rf ./content/*
	cp -r ~/Documents/Notes/public ./content/
	cp ~/Documents/Notes/_index.md ./content/
	cp ~/Documents/Notes/now.md ./content/

fix-content: update-content
	python3 frontmatter_fixer.py
	python3 link_fixer.py

# depends on update-content
build: update-content fix-content
	~/go/bin/hugo-obsidian -input=content -output=data -index=true -root=.

serve: build
	hugo serve
