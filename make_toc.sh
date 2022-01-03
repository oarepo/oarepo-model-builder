#!/bin/bash

echo README.md
md_toc -p github README.md
for d in docs/*md; do
  echo $d
  md_toc -p github $d
done
