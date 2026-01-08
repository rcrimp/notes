---
title: "Running Quartz"
---
Running Quartz

`sudo apt install golang`

`go install github.com/jackyzha0/hugo-obsidian@latest`

``~/go/bin/hugo-obsidian -input=content/ -output=data -index -root=.``

`hugo serve`

## Editing in VS Code
`sudo npm install -g prettier prettier-plugin-go-template`

## Syncing files
from GitHub/notes/
```
cd /home/rcrimp/GitHub/notes/ && \
rsync -avu --delete \
	~/comedy-notes/content/public/ \
	content/public/ && \
rsync -avu --delete \
	~/comedy-notes/content/_index.md \
	content/_index.md && \
rsync -avu --delete \
	~/comedy-notes/content/now.md \
	content/now.md && \
~/go/bin/hugo-obsidian -input=content -output=data -index -root=.

```