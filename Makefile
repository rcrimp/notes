.DEFAULT_GOAL := test

help: ## Show all Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


all-hashed: # builds the site with private files hashed, public files normal
	cd /home/rcrimp/GitHub/notes/ \
   && rsync -avu --delete ~/comedy-notes/content/ content/ \
   && ~/GitHub/hugo-obsidian/hugo-obsidian -input=content -output=data -index -root=. \
   && hugo serve \

all-open: # builds the site with all files
	cd /home/rcrimp/GitHub/notes/ \
   && rsync -avu --delete ~/comedy-notes/content/ content/ \
   && ~/go/bin/hugo-obsidian -input=content -output=data -index -root=. \
   && hugo serve \


public-only: # builds the site with public files
	cd /home/rcrimp/GitHub/notes/ \
   && rm -rf content/* \
   && mkdir content/public/ \
   && rsync -avu --delete ~/comedy-notes/content/public/ content/public/ \
   && rsync -avu --delete ~/comedy-notes/content/_index.md content/_index.md \
   && rsync -avu --delete ~/comedy-notes/content/now.md content/now.md \
   && ~/go/bin/hugo-obsidian -input=content -output=data -index -root=. \
   && hugo serve \

serve:
	hugo serve

# Makefile:34: *** missing separator.  Stop.
test:
	rm -rf ./content/*
	cp -r ~/Documents/Notes/public ./content/
	cp ~/Documents/Notes/_index.md ./content/
	cp ~/Documents/Notes/now.md ./content/
	python3 frontmatter_fixer.py
	python3 link_fixer.py
	mkdir -p static data
	~/go/bin/hugo-obsidian -input=content -output=data -index=true -root=.
	hugo serve

